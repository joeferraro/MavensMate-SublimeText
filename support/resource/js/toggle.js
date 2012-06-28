// function set_togglable_visibility(dom_id, state) {
//   link = $("toggle_link_" + dom_id);
//   detail_div = $(dom_id)
//   if (state) {
//     link.update("-");
//     detail_div.show();
//   }
//   else
//   {
//     link.update("+");
//     detail_div.hide()
//   }
// }
// 
// function toggle_diff(dom_id) {
//   e = $(dom_id)
//   if (! e.readAttribute("loaded")) {
//     e.update(dispatch({controller: 'diff', action: 'diff', revision: e.readAttribute("rev"), git_path: e.readAttribute("git_path"), path: (e.readAttribute("path") || ""), layout: false}))
//     e.setAttribute("loaded");
//   }
//   
//   set_togglable_visibility( dom_id, ! e.visible() );
// }
// 
// function toggle_log(dom_id) {
//   e = $(dom_id)
//   if (! e.readAttribute("loaded")) {
//     e.update(dispatch({controller: 'log', action: 'log', revisions: e.readAttribute("revisions"), git_path: e.readAttribute("git_path"), path: (e.readAttribute("path") || ""), layout: false}))
//     // e.setAttribute("loaded");
//   }
//   
//   set_togglable_visibility( dom_id, ! e.visible() );
// }
