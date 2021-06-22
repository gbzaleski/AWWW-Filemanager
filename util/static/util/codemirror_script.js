

$(document).ready(() => {
    const codeArea = document.getElementById("codemirror-textarea");
    if (codeArea)
    {
        console.log(codeArea)

        editorCodeMirror = CodeMirror.fromTextArea(codeArea, {
            value: "int myScript()\n{\n\treturn 100;\n}\n",
            mode:  "text/x-csrc",
            lineNumbers: true,
          });
    }
})

function saveCode(token)
{
    if (marked)
    {
        const codeData = editorCodeMirror.getValue()
        // alert(codeData)

        $.ajax({
            url : 'edit-code/',
            type : "POST",
            data : {
                'csrfmiddlewaretoken': token,
                "fileid": idsrc,
                "newcontent": codeData,
            },
            success : function(result) {
            alert(result.msg)
            },
            error : function(error)
            {
            alert("Error occured!")
            }
        });
    }
}