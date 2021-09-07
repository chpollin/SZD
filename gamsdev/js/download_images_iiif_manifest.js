// name: download_images_iiif_manifest.js; 
// author: Christopher Pollin
// date: 2021
// dependencies FileSaver.js; JSZip.js

//////////////////////////////////////////////////////////
// * param: PID of METS object
function download_images_iiif_manifest(PID) {
  // check input
  let pattern = /^(o:)|(context:)[a-zA-Z0-9_.]+$/;
  if(pattern.test(PID))
  {
    setVisible('#loading', true);
    
    // stefanzweig.digital/archive/objects/o:szd.6820/methods/sdef:IIIF/getManifest = https://gams.uni-graz.at/archive/objects/o:szd.6820/methods/sdef:IIIF/getManifest
    const URL = '/archive/objects/' + PID + '/methods/sdef:IIIF/getManifest';
    
    // call the fetch function passing the url of the API as a parameter
    fetch(URL, {method: 'get'})
      .then((response) => response.json()) 
      .then(function(data)
      {
        // adress url to img
        let canvases = data["sequences"][0]["canvases"];

        // the zipping process can take a long time if there is too much data; its still fine with ~100 images and ~100 mb; set a limit to 100 images  
        if(canvases.length <= 100)
        {
         build_zip_download(canvases, PID);   
        }
        else
        {
          alert("This object has more than 100 images and more than 100 MB. This process can take a long time. Be aware that his process works in the background and is limited to your bandwidth.");
          build_zip_download(canvases, PID);  
          setVisible('#loading', false)
        }
      })
    //
    .catch(function(error) 
    {
      console.log('Request failed', error)  
    });       
  }
  // pattern.test(PID)
  else
  {
    alert("bitte gib der GAMS echte PIDs\n so wie 'o:depcha.schlitz.1'");
  }
}

function build_zip_download(canvases, PID) {

    let zip = new JSZip();
    // "o:szd.6814" --> szd_6814_images.zip 
    const filename = (PID.replace(".", "_")).replace("o:", "");
    const zipFilename = filename + "_images.zip";

    // for each "https://gams.uni-graz.at/o:szd.6814/canvas/DIV.290""
    for (canvase in canvases)
    {
        // build "https://gams.uni-graz.at/o:szd.6814/IMG.290" --> url to img
        let n = canvases[canvase]["@id"].split('DIV.')[1];
        let imageSrc = "/" + PID + '/IMG.' + n;
        // fetch image via url and make a blob
        let imageBlob = downloadImage(imageSrc, filename);
        // add blob zu zip
        zip.file(`${filename + "_" + n}.jpg`, imageBlob, {binary:true});
        
    }
    // generate zip and download it. the .zip contains all images from the iiif manifest
    zip.generateAsync({type:'blob'}).then(function(content) 
    {
        saveAs(content, zipFilename);
        alert(`Download of ${PID} is ready!`);
        setVisible('#loading', false)
    }); 
}

//////////////////////////////////////////////////////////
// * param: the URL to an image like https://gams.uni-graz.at/o:szd.6814/IMG.290
// this must be in a function because its asnyc
async function downloadImage(imageSrc) {
  const image = await fetch(imageSrc);
  const imageBlob = await image.blob();
  return imageBlob;  
}



