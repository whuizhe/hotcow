function compare(orig,obj){
    var value=orig[0], orig1=orig[2]?orig[2]:null, orig2=orig[1], dv, panes = orig.length, highlight = true, connect = null, collapse = false;
    function initUI() {
    if (value == null) return;
    var target = obj;
    target.innerHTML = "";
    dv = CodeMirror.MergeView(target, {
        value: value,
        origLeft: panes == 3 ? orig1 : null,
        orig: orig2,
        lineNumbers: true,
        mode: "text/html",
        highlightDifferences: highlight,
        connect: connect,
        collapseIdentical: collapse
    });
    }

    function toggleDifferences() {
    dv.setShowDifferences(highlight = !highlight);
    }

    // window.onload = function() {
    // value = "a=2 \nb=3";
    // orig1 = "a=2 \nb=3";
    // orig2 = "b=3 \na=2";
    initUI();
    // };

    function mergeViewHeight(mergeView) {
    function editorHeight(editor) {
        if (!editor) return 0;
        return editor.getScrollInfo().height;
    }
    return Math.max(editorHeight(mergeView.leftOriginal()),
                    editorHeight(mergeView.editor()),
                    editorHeight(mergeView.rightOriginal()));
    }

    function resize(mergeView) {
    var height = mergeViewHeight(mergeView);
    for(;;) {
        if (mergeView.leftOriginal())
        mergeView.leftOriginal().setSize(null, height);
        mergeView.editor().setSize(null, height);
        if (mergeView.rightOriginal())
        mergeView.rightOriginal().setSize(null, height);

        var newHeight = mergeViewHeight(mergeView);
        if (newHeight >= height) break;
        else height = newHeight;
    }
    mergeView.wrap.style.height = height + "px";
    }
}
