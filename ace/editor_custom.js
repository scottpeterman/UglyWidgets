var editor = ace.edit("editor");
editor.setTheme("ace/theme/twilight");
editor.session.setMode("ace/mode/python");
// editor.mode.keyboardHandler.bindKey("ctrl-space", null); // disable ctrl-space
editor.setKeyboardHandler("ace/keyboard/vscode");
//editor.setReadOnly(false);
//editor.session.setOption("autoEscape", false);
//editor.setOption("showInvisibles", true);
//editor.setOption("showPrintMargin", true);
//editor.setOption("enableBasicAutocompletion", false);
//editor.setOption("autoEscape", false);
function replaceSelectionWithDecodedBase64(base64String) {
    console.log(base64String);
    var decodedString = atob(base64String);
    console.log(decodedString);
    editor.session.replace(editor.selection.getRange(), decodedString);
}

editor.commands.addCommand({
    name: 'pasteCommand',
    bindKey: {win: 'Ctrl-V', mac: 'Command-V'},
    exec: function(editor) {
        // Call the paste function in Python
        handler.requestPaste();
        console.log("you requested paste via control-v");
    },
    readOnly: true
});

function set_mode(mode) {
    editor.session.setMode("ace/mode/" + mode);
    if (mode == "json") {
    editor.setOption("showInvisibles", false);
    }
}
editor.commands.addCommand({
    name: "save",
    bindKey: { win: "Ctrl-S", mac: "Command-S" },
    exec: function(editor) {
        // Call your JavaScript function here
//        alert("Saving...");
        handler.saveFromJs();
        print("Javascript save called: saveFromJs in python should fire via pyqtslot")
    }
});
//function fix_autoEscape() {
//    editor.session.setOption("autoEscape", false);
//}
