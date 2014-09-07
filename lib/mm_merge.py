import sublime
import sublime_plugin
import difflib
import re
import os
import subprocess
import threading
from xml.dom import minidom

import MavensMate.config as config

# hack for ST3 to make module load properly
try:
    lock = __file__ + '.lock'

    if not os.path.exists(lock):
        # print("forcing MavensMate Diff to reload itself")
        handle = open(lock, 'w')
        handle.write('')
        handle.close()

        handle = open(__file__, 'r')
        contents = handle.read()
        handle.close()

        handle = open(__file__, 'w')
        handle.write(contents)
        handle.close();
    else:
        os.remove(lock)
except:
    pass
    # print("could not force MavensMate Diff to reload")
# end hack

mmDiffView = None

def executeShellCmd(exe, cwd):
    print ("Cmd: %s" % (exe))
    print ("Dir: %s" % (cwd))

    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, shell=True)

    for line in p.stdout.readlines():
        line = str(line, 'utf-8')
        line = re.sub('(^\s+$)|(\s+$)', '', line)

        if line != '':
            yield line


class MavensMateDiffer():

    def process(self, line0, line1, line2):
        if line0 == None:
            return

        change = line0[0]
        line0 = line0[2:len(line0)]

        part = None

        if change == '+':
            part = {'+': line0, '-': '', 'change': '+', 'intraline': '', 'intralines': {'+': [], '-': []}}

        elif change == '-':
            part = {'-': line0, '+': '', 'change': '-', 'intraline': '', 'intralines': {'+': [], '-': []}}

        elif change == ' ':
            part = line0

        elif change == '?':
            return

        if isinstance(part, str) and (self.lastIdx in self.data) and isinstance(self.data[self.lastIdx], str):
            self.data[self.lastIdx] += part
        else:
            if isinstance(part, dict):
                if line1 and line1[0] == '?':
                    part['intraline'] = change

                if self.lastIdx >= 0:
                    last = self.data[self.lastIdx]
                else:
                    last = None

                if isinstance(last, dict):
                    skip = False

                    im_p = last['intraline'] == '-' and part['change'] == '+'
                    im_ip = last['intraline'] == '-' and part['intraline'] == '+'
                    m_ip = last['change'] == '-' and part['intraline'] == '+'

                    if im_p or im_ip or m_ip:
                        self.data[self.lastIdx]['+'] += part['+']
                        self.data[self.lastIdx]['-'] += part['-']
                        self.data[self.lastIdx]['intraline'] = '!'
                        skip = True
                    elif part['intraline'] == '' and last['intraline'] == '':
                        nextIntraline = None
                        if line2 and line2[0] == '?':
                            nextIntraline = line1[0]

                        if nextIntraline == '+' and part['change'] == '-':
                            self.data.append(part)
                            self.lastIdx += 1
                            skip = True
                        else:
                            self.data[self.lastIdx]['+'] += part['+']
                            self.data[self.lastIdx]['-'] += part['-']
                            skip = True

                    if not skip:
                        self.data.append(part)
                        self.lastIdx += 1
                else:
                    self.data.append(part)
                    self.lastIdx += 1
            else:
                self.data.append(part)
                self.lastIdx += 1

    def difference(self, text1, text2):
        self.data = []
        self.lastIdx = -1
        gen = difflib.Differ().compare(text1.splitlines(1), text2.splitlines(1))

        line0 = None
        line1 = None
        line2 = None

        try:
            line0 = gen.next()
            line1 = gen.next()
        except:
            pass

        inFor = False

        for line2 in gen:
            self.process(line0, line1, line2)
            line0 = line1
            line1 = line2
            inFor = True

        self.process(line0, line1, None)

        if not inFor:
            self.process(line1, line2, None)

        self.process(line2, None, None)

        return self.data


class MavensMateDifferScrollSync():
    left = None
    right = None
    scrollingView = None
    viewToSync = None
    lastPosLeft = None
    lastPosRight = None
    isRunning = False
    last = None
    targetPos = None

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.sync()

    def sync(self):
        beginLeft = self.left.viewport_position()
        beginRight = self.right.viewport_position()

        if not self.isRunning:
            if beginLeft[0] != beginRight[0] or beginLeft[1] != beginRight[1]:
                if self.lastPosLeft == None or (self.lastPosLeft[0] != beginLeft[0] or self.lastPosLeft[1] != beginLeft[1]):
                    self.isRunning = True
                    self.scrollingView = self.left
                    self.viewToSync = self.right

                elif self.lastPosRight == None or (self.lastPosRight[0] != beginRight[0] or self.lastPosRight[1] != beginRight[1]):
                    self.isRunning = True
                    self.scrollingView = self.right
                    self.viewToSync = self.left

        else:
            pos = self.scrollingView.viewport_position()

            if self.targetPos == None and self.last != None and pos[0] == self.last[0] and pos[1] == self.last[1]:
                ve = self.viewToSync.viewport_extent()
                le = self.viewToSync.layout_extent()

                self.targetPos = (max(0, min(pos[0], le[0] - ve[0])), max(0, min(pos[1], le[1] - ve[1])))
                self.viewToSync.set_viewport_position(self.targetPos)

            elif self.targetPos != None:
                poss = self.viewToSync.viewport_position()

                if poss[0] == self.targetPos[0] and poss[1] == self.targetPos[1]:
                    self.isRunning = False
                    self.targetPos = None
                    self.scrollingView = None
                    self.viewToSync = None

            self.last = pos

        self.lastPosRight = beginRight
        self.lastPosLeft = beginLeft

        if self.left.window() != None and self.right.window() != None:
            sublime.set_timeout(self.sync, 100)

class MavensMateDiffViewEraseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.erase(edit, sublime.Region(0, self.view.size()))

class MavensMateDiffViewAppend(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.insert(edit, self.view.size(), text)

class MavensMateDiffViewReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, begin, end, text):
        print('running replace command!')
        self.view.replace(edit, sublime.Region(begin, end), text)

class MavensMateDiffView():
    left = None
    right = None
    origin_window = None
    window = None
    currentDiff = -1
    regions = []
    currentRegion = None
    scrollSyncRunning = False
    lastLeftPos = None
    lastRightPos = None
    diff = None
    createdPositions = False
    lastSel = {'regionLeft': None, 'regionRight': None}
    leftEnabled = True
    rightEnabled = True

    def __init__(self, window, left, right, diff, leftTmp=False, rightTmp=False):
        print('viewing diff')
        #print(window)
        #print(left)
        #print(right)
        #print(diff)
        #print(leftTmp)
        #print(rightTmp)
        self.origin_window = window
        window.run_command('new_window')
        self.window = sublime.active_window()
        self.diff = diff
        self.leftTmp = leftTmp
        self.rightTmp = rightTmp

        if (config.merge_settings.get('hide_side_bar')):
            self.window.run_command('toggle_side_bar')

        self.window.set_layout({
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
        })

        if not isinstance(left, sublime.View):
            self.left = self.window.open_file(left)
            self.leftEnabled = False
        else:
            self.left = self.window.open_file(left.file_name())

        if not isinstance(right, sublime.View):
            self.right = self.window.open_file(right)
            #self.rightEnabled = False
        else:
            self.right = self.window.open_file(right.file_name())

        if not self.rightEnabled and self.rightTmp:
            self.right.set_syntax_file(self.left.settings().get('syntax'))

        if not self.leftEnabled and self.leftTmp:
            self.left.set_syntax_file(self.right.settings().get('syntax'))

        self.left.set_scratch(True)
        self.right.set_scratch(True)

        self.clear()

    def clear(self):
        if self.rightTmp and os.path.exists(self.right.file_name()):
            os.remove(self.right.file_name())

        if self.leftTmp and os.path.exists(self.left.file_name()):
            os.remove(self.left.file_name())

    def enlargeCorrespondingPart(self, part1, part2):
        linesPlus = part1.splitlines()
        linesMinus = part2.splitlines()

        diffLines = len(linesPlus) - len(linesMinus)

        if diffLines < 0:  # linesPlus < linesMinus
            for i in range(-diffLines):
                linesPlus.append('?')

        elif diffLines > 0:  # linesPlus > linesMinus
            for i in range(diffLines):
                linesMinus.append('?')

        result = []

        result.append("\n".join(linesPlus) + "\n")
        result.append("\n".join(linesMinus) + "\n")

        return result

    def loadDiff(self):
        #print('LOADING DIFF!!!!!!')
        self.window.set_view_index(self.right, 1, 0)
        sublime.set_timeout(lambda: self.insertDiffContents(self.diff), 5)

    def insertDiffContents(self, diff):
        left = self.left
        right = self.right

        # edit = left.begin_edit(0, '')
        # left.erase(edit, sublime.Region(0, left.size()))
        # left.end_edit(edit)
        left.run_command('mavens_mate_diff_view_erase')
        right.run_command('mavens_mate_diff_view_erase')
        # edit = right.begin_edit(0, '')
        # right.erase(edit, sublime.Region(0, right.size()))
        # right.end_edit(edit)

        regions = []
        i = 0

        for part in diff:
            if not isinstance(part, dict):
                left.run_command('mavens_mate_diff_view_append', {'text': part})
                right.run_command('mavens_mate_diff_view_append', {'text': part})
                # edit = left.begin_edit(0, '')
                # left.insert(edit, left.size(), part)
                # left.end_edit(edit)

                # edit = right.begin_edit(0, '')
                # right.insert(edit, right.size(), part)
                # right.end_edit(edit)
            else:
                ignore = False

                if config.merge_settings.get('ignore_whitespace'):
                    trimRe = '(^\s+)|(\s+$)'
                    #print('>>>>> START ',re.sub(trimRe, '', part['+']))
                    #print('>>>>> END ',re.sub(trimRe, '', part['-']))
                    if re.sub(trimRe, '', part['+'], flags=re.MULTILINE) == re.sub(trimRe, '', part['-'], flags=re.MULTILINE):
                        ignore = True

                if ignore:
                    # edit = left.begin_edit(0, '')
                    # left.insert(edit, left.size(), part['-'])
                    # left.end_edit(edit)
                    left.run_command('mavens_mate_diff_view_append', {'text': part['-']})
                    right.run_command('mavens_mate_diff_view_append', {'text': part['+']})
                    # edit = right.begin_edit(0, '')
                    # right.insert(edit, right.size(), part['+'])
                    # right.end_edit(edit)
                    continue

                pair = {
                    'regionLeft': None,
                    'regionRight': None,
                    'name': 'diff' + str(i),
                    'mergeLeft': part['+'][:],
                    'mergeRight': part['-'][:],
                    'intralines': {'left': [], 'right': []}
                }

                i += 1

                # edit = left.begin_edit(0, '')
                leftStart = left.size()

                if part['+'] != '' and part['-'] != '' and part['intraline'] != '':
                    inlines = list(difflib.Differ().compare(part['-'].splitlines(1), part['+'].splitlines(1)))
                    begins = {'+': 0, '-': 0}
                    lastLen = 0
                    lastChange = None

                    for inline in inlines:
                        change = inline[0:1]
                        inline = inline[2:len(inline)]
                        inlineLen = len(inline)

                        if change != '?':
                            begins[change] += inlineLen
                            lastLen = inlineLen
                            lastChange = change
                        else:
                            for m in re.finditer('([+-^]+)', inline):
                                sign = m.group(0)[0:1]

                                if sign == '^':
                                    sign = lastChange

                                start = begins[sign] - lastLen + m.start()
                                end = begins[sign] - lastLen + m.end()

                                part['intralines'][sign].append([start, end])

                enlarged = self.enlargeCorrespondingPart(part['+'], part['-'])

                # left.insert(edit, leftStart, enlarged[1])
                # left.end_edit(edit)
                left.run_command('mavens_mate_diff_view_append', {'text': enlarged[1]})

                # edit = right.begin_edit(0, '')
                rightStart = right.size()
                # right.insert(edit, rightStart, enlarged[0])
                # right.end_edit(edit)
                right.run_command('mavens_mate_diff_view_append', {'text': enlarged[0]})

                pair['regionLeft'] = sublime.Region(leftStart, leftStart + len(left.substr(sublime.Region(leftStart, left.size()))))
                pair['regionRight'] = sublime.Region(rightStart, rightStart + len(right.substr(sublime.Region(rightStart, right.size()))))

                if pair['regionLeft'] != None and pair['regionRight'] != None:
                    for position in part['intralines']['-']:
                        change = sublime.Region(leftStart + position[0], leftStart + position[1])
                        pair['intralines']['left'].append(change)

                    for position in part['intralines']['+']:
                        change = sublime.Region(rightStart + position[0], rightStart + position[1])
                        pair['intralines']['right'].append(change)

                    regions.append(pair)

        for pair in regions:
            self.createDiffRegion(pair)

        self.createdPositions = True

        self.regions = regions
        sublime.set_timeout(lambda: self.selectDiff(0), 100)  # for some reason this fixes the problem to scroll both views to proper position after loading diff

        self.left.set_read_only(True)
        self.right.set_read_only(True)
        MavensMateDifferScrollSync(self.left, self.right)

    def createDiffRegion(self, region):
        rightScope = leftScope = config.merge_settings.get('diff_region_scope')

        if region['mergeLeft'] == '':
            rightScope = config.merge_settings.get('diff_region_removed_scope')
            leftScope = config.merge_settings.get('diff_region_added_scope')
        elif region['mergeRight'] == '':
            leftScope = config.merge_settings.get('diff_region_removed_scope')
            rightScope = config.merge_settings.get('diff_region_added_scope')

        if not self.createdPositions:
            print('intralines' + region['name'], region['intralines']['left'], config.merge_settings.get('diff_region_change_scope'))
            print('intralines' + region['name'], region['intralines']['right'], config.merge_settings.get('diff_region_change_scope'))
            self.left.add_regions('intralines' + region['name'], region['intralines']['left'], config.merge_settings.get('diff_region_change_scope'))
            self.right.add_regions('intralines' + region['name'], region['intralines']['right'], config.merge_settings.get('diff_region_change_scope'))

        self.left.add_regions(region['name'], [region['regionLeft']], leftScope, config.merge_settings.get('diff_region_gutter_icon'), sublime.DRAW_OUTLINED)
        self.right.add_regions(region['name'], [region['regionRight']], rightScope, config.merge_settings.get('diff_region_gutter_icon'), sublime.DRAW_OUTLINED)

    def createSelectedRegion(self, region):
        self.left.add_regions(region['name'], [region['regionLeft']], config.merge_settings.get('selected_diff_region_scope'), config.merge_settings.get('selected_diff_region_gutter_icon'))
        self.right.add_regions(region['name'], [region['regionRight']], config.merge_settings.get('selected_diff_region_scope'), config.merge_settings.get('selected_diff_region_gutter_icon'))

    def selectDiff(self, diffIndex):
        if diffIndex >= 0 and diffIndex < len(self.regions):
            self.left.sel().clear()
            self.left.sel().add(sublime.Region(0, 0))
            self.right.sel().clear()
            self.right.sel().add(sublime.Region(0, 0))

            if self.currentRegion != None:
                self.createDiffRegion(self.currentRegion)

            self.currentRegion = self.regions[diffIndex]
            self.createSelectedRegion(self.currentRegion)

            self.currentDiff = diffIndex

            self.left.show_at_center(sublime.Region(self.currentRegion['regionLeft'].begin(), self.currentRegion['regionLeft'].begin()))
            if not config.merge_settings.get('ignore_whitespace'):  # @todo: temporary fix for loosing view sync while ignore_whitespace is true
                self.right.show_at_center(sublime.Region(self.currentRegion['regionRight'].begin(), self.currentRegion['regionRight'].begin()))

    def selectDiffUnderSelection(self, selection, side):
        if self.createdPositions:
            if selection[0].begin() == 0 and selection[0].end() == 0:  # this fixes strange behavior with regions
                return

            for i in range(len(self.regions)):
                if self.regions[i][side].contains(selection[0]):
                    self.selectDiff(i)
                    break

    def checkForClick(self, view):
        side = None

        if view.id() == self.left.id():
            side = 'regionLeft'
        elif view.id() == self.right.id():
            side = 'regionRight'

        if side != None:
            sel = [r for r in view.sel()]

            if self.lastSel[side]:
                if sel == self.lastSel[side]:  # previous selection equals current so it means this was a mouse click!
                    self.selectDiffUnderSelection(view.sel(), side)

            self.lastSel[side] = sel

    def goUp(self):
        self.selectDiff(self.currentDiff - 1)

    def goDown(self):
        self.selectDiff(self.currentDiff + 1)

    def mergeDisabled(self, direction):
        print('checking if merge is disabled: ', direction)
        print(not self.rightEnabled and direction == '>>') or (not self.leftEnabled and direction == '<<')
        return (not self.rightEnabled and direction == '>>') or (not self.leftEnabled and direction == '<<')

    def merge(self, direction, mergeAll):
        print('mm merging!', direction)
        
        target_is_server_copy = False

        if self.mergeDisabled(direction):
            return

        if mergeAll:
            print('merging all!', direction)
            while len(self.regions) > 0:
                self.merge(direction, False)
            return

        if (self.currentRegion != None):
            lenLeft = self.left.size()
            lenRight = self.right.size()
            if direction == '<<':
                source = self.right
                target = self.left
                sourceRegion = self.currentRegion['regionRight']
                targetRegion = self.currentRegion['regionLeft']
                contents = self.currentRegion['mergeLeft']

            elif direction == '>>':
                target_is_server_copy = True
                source = self.left
                target = self.right
                sourceRegion = self.currentRegion['regionLeft']
                targetRegion = self.currentRegion['regionRight']
                contents = self.currentRegion['mergeRight']

            target.set_scratch(True)

            target.set_read_only(False)
            source.set_read_only(False)

            print('about to run target command', target)
            # edit = target.begin_edit(0, '')
            # target.replace(edit, targetRegion, contents)
            # target.end_edit(edit)
            target.run_command('mavens_mate_diff_view_replace', {'begin': targetRegion.begin(), 'end': targetRegion.end(), 'text': contents})

            # edit = source.begin_edit(0, '')
            # source.replace(edit, sourceRegion, contents)
            # source.end_edit(edit)
            print('about to run source command', source)
            source.run_command('mavens_mate_diff_view_replace', {'begin': sourceRegion.begin(), 'end': sourceRegion.end(), 'text': contents})

            diffLenLeft = self.left.size() - lenLeft
            diffLenRight = self.right.size() - lenRight

            source.erase_regions(self.currentRegion['name'])
            target.erase_regions(self.currentRegion['name'])
            source.erase_regions('intralines' + self.currentRegion['name'])
            target.erase_regions('intralines' + self.currentRegion['name'])

            target.set_scratch(False)

            del self.regions[self.currentDiff]

            for i in range(self.currentDiff, len(self.regions)):
                self.regions[i]['regionLeft'] = self.moveRegionBy(self.regions[i]['regionLeft'], diffLenLeft)
                self.regions[i]['regionRight'] = self.moveRegionBy(self.regions[i]['regionRight'], diffLenRight)

                # for j in range(self.currentDiff, len(self.regions[i]['intralines']['left'])):
                #     self.regions[i]['intralines']['left'][j] = self.moveRegionBy(self.regions[i]['intralines']['left'][j], diffLenLeft)

                # for j in range(self.currentDiff, len(self.regions[i]['intralines']['right'])):
                #     self.regions[i]['intralines']['right'][j] = self.moveRegionBy(self.regions[i]['intralines']['right'][j], diffLenRight)

                if i != self.currentDiff:
                    self.createDiffRegion(self.regions[i])

            #explicitly save the "server/local copy" version (for ux purposes)
            #if target_is_server_copy:
            source.run_command("save")
            target.run_command("save")

            target.set_read_only(True)
            source.set_read_only(True)

            if self.currentDiff > len(self.regions) - 1:
                self.currentDiff = len(self.regions) - 1

            self.currentRegion = None

            if self.currentDiff >= 0:
                self.selectDiff(self.currentDiff)
            else:
                self.currentDiff = -1

            #merge is over
            if self.currentDiff == -1:
                file_name = None
                if target_is_server_copy:
                    file_name = source.file_name()
                else:
                    file_name = target.file_name()
                args = {
                    "files"     : [file_name]
                }
                self.origin_window.run_command('force_compile_file', args)
                sublime.set_timeout(lambda: self.window.run_command('close_window'), 0)

            self.window.focus_view(target)

    def moveRegionBy(self, region, by):
        return sublime.Region(region.begin() + by, region.end() + by)

    def abandonUnmergedDiffs(self, side):
        if side == 'left':
            view = self.left
            regionKey = 'regionLeft'
            contentKey = 'mergeRight'
        elif side == 'right':
            view = self.right
            regionKey = 'regionRight'
            contentKey = 'mergeLeft'

        view.set_read_only(False)
        #edit = view.begin_edit(0, '')

        for i in range(len(self.regions)):
            sizeBefore = view.size()
            #view.replace(edit, self.regions[i][regionKey], self.regions[i][contentKey])
            view.run_command('mavens_mate_diff_view_replace', {'begin': self.regions[i][regionKey].begin(), 'end': self.regions[i][regionKey].end(), 'text': self.regions[i][contentKey]})
            sizeDiff = view.size() - sizeBefore

            if sizeDiff != 0:
                for j in range(i, len(self.regions)):
                    self.regions[j][regionKey] = sublime.Region(self.regions[j][regionKey].begin() + sizeDiff, self.regions[j][regionKey].end() + sizeDiff)

        #view.end_edit(edit)
        view.set_read_only(True)


class ThreadProgress():
    def __init__(self, thread, message):
        self.th = thread
        self.msg = message
        self.add = 1
        self.size = 8
        self.speed = 100
        sublime.set_timeout(lambda: self.run(0), self.speed)

    def run(self, i):
        if not self.th.is_alive():
            if hasattr(self.th, 'result') and not self.th.result:
                sublime.status_message('')
            return

        before = i % self.size
        after = (self.size - 1) - before

        sublime.status_message('%s [%s=%s]' % (self.msg, ' ' * before, ' ' * after))

        if not after:
            self.add = -1
        if not before:
            self.add = 1

        i += self.add

        sublime.set_timeout(lambda: self.run(i), self.speed)

class MavensMateDiffThread(threading.Thread):
    def __init__(self, window, left, right, leftTmp=False, rightTmp=False):
        self.window = window
        self.left = left
        self.right = right
        self.leftTmp = leftTmp
        self.rightTmp = rightTmp

        #self.text1 = self.left.substr(sublime.Region(0, self.left.size()))

        if not isinstance(self.left, sublime.View):
            self.text1 = open(self.left, 'rb').read().decode('utf-8', 'replace')
        else:
            self.text1 = self.left.substr(sublime.Region(0, self.left.size()))
            if self.left.is_dirty():
                self.leftTmp = True

        if not isinstance(self.right, sublime.View):
            self.text2 = open(self.right, 'rb').read().decode('utf-8', 'replace')
        else:
            self.text2 = self.right.substr(sublime.Region(0, self.right.size()))
            if self.right.is_dirty():
                self.rightTmp = True

        # print('left: ', self.left)
        # print('right: ', self.right)
        # print('ltmp: ', self.leftTmp)
        # print('rtmp: ', self.rightTmp)

        threading.Thread.__init__(self)

    def run(self):
        ThreadProgress(self, 'Computing differences')

        global mmDiffView

        differs = False

        if config.merge_settings.get('ignore_crlf'):
            self.text1 = re.sub('\r\n', '\n', self.text1)
            self.text2 = re.sub('\r\n', '\n', self.text2)

            self.text1 = re.sub('\r', '\n', self.text1)
            self.text2 = re.sub('\r', '\n', self.text2)

        if config.merge_settings.get('ignore_whitespace'):
            regexp = re.compile('(^\s+)|(\s+$)', re.MULTILINE)
            if re.sub(regexp, '', self.text1) != re.sub(regexp, '', self.text2):
                differs = True
        elif self.text1 != self.text2:
            differs = True

        if not differs:
            sublime.error_message('There is no difference between files')
            if self.leftTmp and not isinstance(self.left, sublime.View):
                os.remove(self.left)
            if self.rightTmp and not isinstance(self.right, sublime.View):
                os.remove(self.right)
            
            args = {
                "files"     : [self.left.file_name()]
            }
            self.window.run_command('force_compile_file', args)
            
            return

        diff = MavensMateDiffer().difference(self.text1, self.text2)
        def inner():
            global mmDiffView
            mmDiffView = MavensMateDiffView(self.window, self.left, self.right, diff, self.leftTmp, self.rightTmp)

        sublime.set_timeout(inner, 100)

class MavensMateDiffCommand(sublime_plugin.WindowCommand):
    viewsPaths = []
    viewsList = []
    itemsList = []
    commits = []
    window = None
    view = None

    def is_enabled(self):
        view = sublime.active_window().active_view();
        if mmDiffView and  mmDiffView.left and mmDiffView.right and view and (view.id() == mmDiffView.left.id() or view.id() == mmDiffView.right.id()):
            return False
        if mmDiffView:
            return True
        else:
            return False

    def getComparableFiles(self):
        self.viewsList = []
        self.viewsPaths = []
        active = self.window.active_view()

        allViews = self.window.views()
        ratios = []
        if config.merge_settings.get('intelligent_files_sort'):
            original = os.path.split(active.file_name())

        for view in allViews:
            if view.file_name() != None and view.file_name() != active.file_name() and (not config.merge_settings.get('same_syntax_only') or view.settings().get('syntax') == active.settings().get('syntax')):
                f = view.file_name()

                ratio = 0

                if config.merge_settings.get('intelligent_files_sort'):
                    ratio = difflib.SequenceMatcher(None, original[1], os.path.split(f)[1]).ratio()

                ratios.append({'ratio': ratio, 'file': f, 'dirname': ''})

        ratiosLength = len(ratios)

        if ratiosLength > 0:
            ratios = sorted(ratios, key=self.cmp_to_key(self.sortFiles))

            if config.merge_settings.get('compact_files_list'):
                for i in range(ratiosLength):
                    for j in range(ratiosLength):
                        if i != j:
                            sp1 = os.path.split(ratios[i]['file'])
                            sp2 = os.path.split(ratios[j]['file'])

                            if sp1[1] == sp2[1]:
                                ratios[i]['dirname'] = self.getFirstDifferentDir(sp1[0], sp2[0])
                                ratios[j]['dirname'] = self.getFirstDifferentDir(sp2[0], sp1[0])

            for f in ratios:
                self.viewsPaths.append(f['file'])
                self.viewsList.append(self.prepareListItem(f['file'], f['dirname']))

            sublime.set_timeout(lambda: self.window.show_quick_panel(self.viewsList, self.onListSelect), 0) #timeout for ST3
        else:
            # if config.merge_settings.get('same_syntax_only'):
            #     syntax = re.match('(.+)\.tmLanguage$', os.path.split(active.settings().get('syntax'))[1])
            #     if syntax != None:
            #         sublime.error_message('There are no other open ' + syntax.group(1) + ' files to compare')
            #         return

            sublime.error_message('There are no other open files to compare')

    def run(self):
        self.window = sublime.active_window()
        self.active = self.window.active_view()

        if not self.active or self.active.file_name() is None:
            return

        sp = os.path.split(self.active.file_name())

        def onMenuSelect(index):
            if index == 0:
                self.getComparableFiles()

        items = ['Compare to other file...']

        if len(items) > 1:
            sublime.set_timeout(lambda: self.window.show_quick_panel(items, onMenuSelect), 0)
        else:
            self.getComparableFiles()

    def displayQuickPanel(self, commitStack, callback):
        sublime.status_message('')

        self.itemsList = []
        self.commits = []
        for item in commitStack:
            self.commits.append(item['commit'])
            itm = [item['commit'][0:10] + ' @ ' + item['date'], item['author']]
            line = ""
            if len(item['msg']) > 0:
                line = re.sub('(^\s+)|(\s+$)', '', item['msg'][0])
            
            itm.append(line)

            self.itemsList.append(itm)

        self.window.show_quick_panel(self.itemsList, callback)

    def prepareListItem(self, name, dirname):
        if config.merge_settings.get('compact_files_list'):
            sp = os.path.split(name)

            if dirname != None and dirname != '':
                dirname = ' / ' + dirname
            else:
                dirname = ''

            if (len(sp[0]) > 56):
                p1 = sp[0][0:20]
                p2 = sp[0][-36:]
                return [sp[1] + dirname, p1 + '...' + p2]
            else:
                return [sp[1] + dirname, sp[0]]
        else:
            return name

    def getFirstDifferentDir(self, a, b):
        a1 = re.split('[/\\\]', a)
        a2 = re.split('[/\\\]', b)

        len2 = len(a2) - 1

        for i in range(len(a1)):
            if i > len2 or a1[i] != a2[i]:
                return a1[i]

    def cmp_to_key(self, mycmp):
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K

    def sortFiles(self, a, b):
        d = b['ratio'] - a['ratio']

        if d == 0:
            return 0
        if d < 0:
            return -1
        if d > 0:
            return 1

    def onListSelect(self, itemIndex):
        if itemIndex > -1:
            allViews = self.window.views()
            compareTo = None
            for view in allViews:
                if (view.file_name() == self.viewsPaths[itemIndex]):
                    compareTo = view
                    break

            if compareTo != None:
                global mmDiffView

                th = MavensMateDiffThread(self.window, self.window.active_view(), compareTo)
                th.start()


class MavensMateDiffGoUpCommand(sublime_plugin.WindowCommand):
    def run(self):
        if mmDiffView != None:
            mmDiffView.goUp()

    def is_visible(self):
        view = sublime.active_window().active_view();
        if mmDiffView and mmDiffView.left and mmDiffView.right and view and (view.id() == mmDiffView.left.id() or view.id() == mmDiffView.right.id()):
            return True

        return False

    def is_enabled(self):
        return self.is_visible() and len(mmDiffView.regions) > 1 and mmDiffView.currentDiff > 0


class MavensMateDiffGoDownCommand(sublime_plugin.WindowCommand):
    def run(self):
        if mmDiffView != None:
            mmDiffView.goDown()

    def is_visible(self):
        view = sublime.active_window().active_view();
        if mmDiffView and mmDiffView.left and mmDiffView.right and view and (view.id() == mmDiffView.left.id() or view.id() == mmDiffView.right.id()):
            return True

        return False

    def is_enabled(self):
        return self.is_visible() and mmDiffView.currentDiff < len(mmDiffView.regions) - 1


class MavensMateDiffMergeLeftCommand(sublime_plugin.WindowCommand):
    def run(self, mergeAll=False):
        if mmDiffView != None:
            mmDiffView.merge('<<', mergeAll)

    def is_visible(self):
        view = sublime.active_window().active_view();
        if mmDiffView and mmDiffView.left and mmDiffView.right and view and (view.id() == mmDiffView.left.id() or view.id() == mmDiffView.right.id()) and not mmDiffView.mergeDisabled('<<'):
            return True

        return False

    def is_enabled(self):
        return self.is_visible() and len(mmDiffView.regions) > 0

class MavensMateDiffMergeRightCommand(sublime_plugin.WindowCommand):
    def run(self, mergeAll=False):
        if mmDiffView != None:
            mmDiffView.merge('>>', mergeAll)

    def is_visible(self):
        view = sublime.active_window().active_view();
        if mmDiffView and mmDiffView.left and mmDiffView.right and view and (view.id() == mmDiffView.left.id() or view.id() == mmDiffView.right.id()) and not mmDiffView.mergeDisabled('>>'):
            return True

        return False

    def is_enabled(self):
        return self.is_visible() and len(mmDiffView.regions) > 0
        
class MavensMateDiffSelectedFiles(sublime_plugin.WindowCommand):
    def run(self, files):
        allViews = self.window.views()
        for view in allViews:
            if view.file_name() == files[0]:
                files[0] = view

            if view.file_name() == files[1]:
                files[1] = view

        th = MavensMateDiffThread(self.window, files[0], files[1])
        th.start()

    def is_enabled(self, files):
        return len(files) == 2

class MavensMateDiffFromSidebar(sublime_plugin.WindowCommand):
    def is_enabled(self, files):
        return len(files) == 1

    def run(self, files):
        sublime.active_window().open_file(files[0], sublime.TRANSIENT)
        sublime.active_window().run_command('mavens_mate_diff')

class MavensMateDiffOverwriteServerCopy(sublime_plugin.WindowCommand):
    def run(self):
        if mmDiffView != None:
            args = {
                "files"     : [mmDiffView.left.file_name()]
            }
            mmDiffView.origin_window.run_command('force_compile_file', args)
            sublime.set_timeout(lambda: mmDiffView.window.run_command('close_window'), 0)

    def is_enabled(self):
        if mmDiffView == None:
            return False
        elif mmDiffView.window == None:
            return False
        else:
            return True

class MavensMateDiffListener(sublime_plugin.EventListener):
    left = None
    right = None

    def on_load(self, view):
        global mmDiffView

        if mmDiffView != None:
            if view.id() == mmDiffView.left.id():
                #print("Left file: " + view.file_name())
                self.left = view

            elif view.id() == mmDiffView.right.id():
                #print("Right file: " + view.file_name())
                self.right = view

            if self.left != None and self.right != None:
                mmDiffView.loadDiff()
                self.left = None
                self.right = None

    def on_pre_save(self, view):
        global mmDiffView

        if (mmDiffView):
            if view.id() == mmDiffView.left.id():
                mmDiffView.abandonUnmergedDiffs('left')

            elif view.id() == mmDiffView.right.id():
                mmDiffView.abandonUnmergedDiffs('right')

    def on_post_save(self, view):
        global mmDiffView

        if mmDiffView and (view.id() == mmDiffView.left.id() or view.id() == mmDiffView.right.id()):
            if mmDiffView.currentDiff == -1: #done diffing
                mmDiffView.clear()
                wnd = view.window()
                if view.id() == mmDiffView.left.id():
                    args = {
                        "files"     : [mmDiffView.left.file_name()]
                    }
                    mmDiffView.origin_window.run_command('force_compile_file', args)
                #if wnd:
                    sublime.set_timeout(lambda: wnd.run_command('close_window'), 0)

    def on_pre_close(self, view):
        global mmDiffView
        wnd = view.window()
        if mmDiffView != None:
            wnd.run_command("save_all")

    def on_close(self, view):
        global mmDiffView

        if mmDiffView != None:
            if view.id() == mmDiffView.left.id():
                mmDiffView.clear()
                wnd = mmDiffView.right.window()
                if wnd != None:
                    sublime.set_timeout(lambda: wnd.run_command('close_window'), 0)
                mmDiffView = None

            elif view.id() == mmDiffView.right.id():
                mmDiffView.clear()
                wnd = mmDiffView.left.window()
                if wnd != None:
                    sublime.set_timeout(lambda: wnd.run_command('close_window'), 0)
                mmDiffView = None

    def on_selection_modified(self, view):
        if mmDiffView:
            mmDiffView.checkForClick(view)