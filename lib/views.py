def get_view_by_group_index(window, group, index):
    groups = {0: {}}
    last_group = 0
    start_index = 0
    iter_index = 0
    original_view = window.active_view()
    original_views = {}
    for iter_group in xrange(window.num_groups()):
        window.focus_group(iter_group)
        original_views[iter_group] = window.active_view()
        groups[iter_group] = {}

    for view in window.views():
        if window.num_groups() == 1:
            groups[group][iter_index] = view
        else:
            window.focus_view(view)
            id = view.id()
            iter_group = last_group
            while iter_group < window.num_groups():
                window.focus_group(iter_group)
                active_view = window.active_view()
                if active_view and active_view.id() == id:
                    if len(groups) == iter_group:
                        groups[iter_group] = {}
                    groups[iter_group][iter_index - start_index] = view
                    break
                iter_group += 1
                last_group = iter_group
                start_index = iter_index

        iter_index += 1

    for iter_group in original_views:
        if not original_views[iter_group]:
            continue
        window.focus_view(original_views[iter_group])

    window.focus_view(original_view)
    return groups[group][index]


def get_all_views(window):
    views = window.views()
    active_view = window.active_view()
    if active_view and active_view.id() not in [ view.id() for view in views ]:
        views.append(active_view)
    return views
