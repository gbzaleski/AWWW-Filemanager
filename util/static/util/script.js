var editorCodeMirror;

function putInput(path, holdername)
{
   if (path.length > 1 && holdername) 
        jQuery.get(path, function(txt)
        {
           $('#' + holdername).html(txt);
        });
}

function putCode(path, holdername)
{
   if (path.length > 1 && holdername) 
        jQuery.get(path, function(txt)
        {
            editorCodeMirror.setValue(txt);
        });
}

var marked = null;
var framapath, framapathsrc, idsrc;
var focushidden = false;
var framaflag = 'frama-c -wp -wp-log="r:result.txt" ';
var toPreload = {};

function markElement(ele, urlpath, _framapath, id)
{
   if (focushidden)
   {
      hideFocus();
   }

  // $('#codeholdplace').text(null);
   $('#focuscontentplace').text(null);

   if (ele == marked)
   {
        ele.style.removeProperty("color");
        editorCodeMirror.setValue("");
        marked = null;
        return;   
   }     

   if (marked)
   {
      marked.style.removeProperty("color");
   }
        
   putCode(urlpath, 'codeholdplace');
   if (toPreload[id])
      _framapath = toPreload[id];
   putInput(_framapath, 'focuscontentplace')

   framapathsrc = _framapath;
   idsrc = id;
   ele.style.color = "blue";
   framapath = urlpath;
   marked = ele;
   
}

function updateFramaShow()
{
   document.getElementById("framacompile").innerHTML = framaflag + "filename.c";
}

function setFramaProp()
{
   framaflag = 'frama-c -wp -wp-prover alt-ergo -wp-prop="-@invariant" ';

   updateFramaShow();
}

function setFramaBasic()
{
   framaflag = 'frama-c -wp -wp-log="r:result.txt" ';

   updateFramaShow();
}

function setFramaRte()
{
   framaflag = 'frama-c -wp -wp-prover alt-ergo -wp-rte ';

   updateFramaShow();
}

function setFramaBoth()
{
   framaflag = 'frama-c -wp -wp-prover alt-ergo -wp-prop="-@invariant" -wp-rte ';

   updateFramaShow();
}

function launchFrama(token)
{
   if (marked == null)
   {
      alert("No files chosen");
      return
   }

   let filename = framapath.substring(framapath.lastIndexOf('/') + 1)
   filename = filename.substring(0, filename.length - 2)

   let purename = filename;
   if (filename.lastIndexOf('_') > 0)
      purename = filename.substring(0, filename.lastIndexOf('_'));
   
   const src = "/media/hard/" + purename + "_frama.txt";

   putInput(src, 'focuscontentplace');

   toPreload[idsrc] = src;
   document.getElementById("fileid").value = idsrc;
   document.getElementById("framapath").value = src;
   //document.getElementById("framaform").submit();

   $.ajax({
      url : 'update-frama/',
      type : "POST",
      data : {
          'csrfmiddlewaretoken': token,
          "fileid": idsrc,
          "framapath": src,
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

function hideFocus()
{
   focushidden = !focushidden;
   $("#focuscontentplace").toggle();
}

function deleteObjFromBoard(id)
{
   console.log("delete: ", id, " ", $("#" + id));
   parent.$("#" + id).hide();
}

function deleteDirectoryJs()
{
   const dirid = 'dir-wrap-' + document.getElementById("dirs").value;
   deleteObjFromBoard(dirid);
}


function deleteFileJs()
{
   const fileid = 'file-' + document.getElementById("files").value;
   deleteObjFromBoard(fileid);
}