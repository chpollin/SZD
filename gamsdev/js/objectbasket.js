// GAMS - OBJECTBASKET

// name: objectbasket.js; 
// author: Christopher Pollin
// date: 2020
// dependencies FileSaver.js; JSZip.js

/* 
 * o:szd.werke --> get METADATA; parse XML; get title, owner, lastmodified, identifier
 * store bit metadata and the object (xml) in local storage (objectbasket); 
 * zip and export everything in (objectbasket)
*/


//EXAMPLES PIDs
// o:iiw.interpreters       TEI
// o:szd.werke              TEI
// o:roth.601129            LIDO
// o:depcha.schlitz.1       TEI
// o:htx.WR1                TEI
// o:szd.2087               METS --> (download all images ?


// TODO
// o:yoda.1373              MEI
// * load a "context" and get all objects connected to this contect; context:depcha.wheaton
// * o:madgwas-skos ; CORS!           SKOS   
// * o:depcha.bookkeeping ; CORS!     ONTOLOGY
// * load all images connected to a METS-File
// * GAMS4+
// * download of a single object in list

//////////////////////////////////////////////////////////
// GLOBAL
var project = "objectbasket";

//////////////////////////////////////////////////////////
// addObject()
// param: text via form or checkbox
function addObject(checkBox) {
  // build URL with text-input (PID) OR parent id (=PID) of the checkbox
  let input_value = document.querySelector("#input1").value || checkBox.parentElement.id;
  // check input
  let pattern = /^(o:)|(context:)[a-zA-Z0-9_.]+$/;
  if(pattern.test(input_value) || checkBox.checked == true)
  {
  // URL
    const BaseURL = "https://glossa.uni-graz.at/";
    const URL = BaseURL + input_value;
    const URL_Metadata = BaseURL + input_value + "/METADATA";
    
    // call the fetch function passing the url of the API as a parameter
    fetch(URL_Metadata, {method: 'get'})
      // transform the data into text
      .then((response) => response.text())
      .then(function(data)
      {
        // parse the response.text as xml
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(data, "text/xml");
       
        // check via model which content model (tei, lido etc.)
        // as there can be multiple <result> in METADATA, select the result with the child <model @uri>
        const result = xmlDoc.querySelector("result > model[uri]").parentElement;
        const model = xmlDoc.querySelector("model[uri]").getAttribute("uri")

        let URL_Source = "";
        switch(model) 
        {
          case 'info:fedora/cm:TEI':
          URL_Source = URL + "/TEI_SOURCE";
          break;
          
          case 'info:fedora/cm:MEI':                  // --> keine Metadata
          URL_Source = URL + "/MEI_SOURCE";
          break;
          
          case 'info:fedora/cm:LIDO':
          URL_Source = URL + "/LIDO_SOURCE";
          break;
          
          case 'info:fedora/cm:Ontology':             // error Cors http - https
          URL_Source = URL + "/ONTOLOGY";
          break;
          
          case 'info:fedora/cm:SKOS':                 // error Cors http - https
          URL_Source = URL + "/ONTOLOGY";
          break;
          
          case 'info:fedora/cm:dfgMETS':
          URL_Source = URL + "/METS_SOURCE";
          break;

          // HTML
          default:
          URL_Source = URL + "";
         } 
         
        // get title, model (info:fedora/cm:TEI), ownerId, lastModifiedDate and identifier from /METADATA
        // write it into an object
        let objectbasketItem = { 
             "title": result.getElementsByTagName("title")[0].childNodes[0].nodeValue, 
             "model" : model,
             "ownerId" : result.getElementsByTagName("ownerId")[0].childNodes[0].nodeValue,
             "lastModifiedDate": result.getElementsByTagName("lastModifiedDate")[0].childNodes[0].nodeValue, 	
             "identifier": result.getElementsByTagName("identifier")[0].childNodes[0].nodeValue,
             "source_url": URL_Source
           } 
         
         ///////////////////////////////////////////
         // add objectbasketItem to the localStorage 
         // the "|| []" replaces possible null from localStorage with empty array
         let objectbasket = JSON.parse(localStorage.getItem(project)) || [];

         let exists = false;
         // check if objectbasket is not empty
         if(typeof objectbasket !== 'undefined' && objectbasket.length > 0)
         {
           // check if item already exists
           for (let count = 0; count < objectbasket.length; count++){
             if(objectbasketItem.identifier == objectbasket[count].identifier){
               exists = true;
               break;
               }
           }
         }
         if(!exists)
         {addTolocalStorage(objectbasketItem);}
      })
    //
    .catch(function(error) 
    {
      console.log('Request failed', error)  
    });         
  }
  else
  {alert("bitte gib der GAMS echte PIDs\n so wie 'o:depcha.schlitz.1'");}
  
  //localStorage needs some time to store the very first item... so wait a bit for it
  setTimeout(function(){
    showData();
  }, 250);
}

//////////////////////////////////////////////////////////
// addTolocalStorage()
// Adds new item to localStorage Array and saves it back to localStorage
function addTolocalStorage(data){
    // the "|| []" replaces possible null from localStorage with empty array
    let objectbasket = JSON.parse(localStorage.getItem(project)) || [];
    objectbasket.push(data);
    localStorage.setItem(project, JSON.stringify(objectbasket));
}

////////////////////////////
//  clearData()
//  clears the localStorage
function clearData()
{
	localStorage.clear();
	location.reload();
}

////////////////////////////
//  zipAndDownload()
//
function zipAndDownload()
{
    // initalize the localStorage-Array     
	let objectbasket = JSON.parse(localStorage.getItem(project)) || [];

	// see jszip.min.js
	const zip = new JSZip();
	const zipFilename = "gamsExport.zip";
	let count = 0;
   
	objectbasket.forEach(item => fetch(item.source_url, {method: 'get',mode: 'cors'})
      .then((response) => response.text())
      .then(function(source)
      {
       
        // o:iiw.interpreters -->  o_iiw_interpreters.xml
        let string_replace =  item.identifier.replace(".", "_");
        let filename = string_replace.replace("o:", "") + ".xml";
        // see jszip.min.js
        zip.file(filename, source, {binary:false}); 
        // just one .zip
        count++;
        if(count === objectbasket.length) 
        {
          zip.generateAsync({type:'blob'}).then(function(content) {
            saveAs(content, zipFilename);
          });
        }
       }));
	 count = 0;
}

////////////////////////////
//  showData()
//
function showData() 
{	
	// initalize the localStorage-Array
    let objectbasket = JSON.parse(localStorage.getItem(project)) || [];
    let objectbasket_tbody = document.getElementById("objectbasket_tbody");
    
    if(!objectbasket_tbody.hasChildNodes())
    {
   	//for every object in the array create a ul = objectbasketLength 
   	for (let count = 0; count < objectbasket.length; count++){
   	    // every row/entry
   		let tr = document.createElement('tr');
   		tr.setAttribute("id", objectbasket[count].identifier);
   		objectbasket_tbody.appendChild(tr);
   		
   		// create tr for every entity
   		tr.appendChild(createTD(objectbasket[count].identifier));
   		tr.appendChild(createTD(objectbasket[count].title));
   		tr.appendChild(createTD(objectbasket[count].model));
   		tr.appendChild(createTD(objectbasket[count].ownerId));
   		tr.appendChild(createTD(objectbasket[count].lastModifiedDate));
           
           // delete button
   		let button_delet = document.createElement('button');
   		button_delet.setAttribute("onclick", "deletItem('" + objectbasket[count].identifier +"')");
   		button_delet.appendChild(document.createTextNode('x'));
   		let td_delete = document.createElement('tr'); 
   		td_delete.appendChild(button_delet);
   		// download button
   	  /*let button_download = document.createElement('button');
   		button_download.setAttribute("onclick", "downloadItem('" + objectbasket[count].identifier +"')");
   		button_download.appendChild(document.createTextNode('download'));
   		td_delete.appendChild(button_download); */
   		tr.appendChild(td_delete);
       }
    }
    // if children exist destroy innerHTML and recreate table content
    else
    {
      objectbasket_tbody.innerHTML = '';
      showData();
    }
}

////////////////////////////
// createTD()
function createTD(content) 
{
  const td = document.createElement('td');
  td.appendChild(document.createTextNode(content));
  return td;
}
////////////////////////////
// downloadItem()
function downloadItem(content) 
{
  console.log('test');
}

////////////////////////////
// deletItem() 
// delets item in objectbasket using splice() to remove it from the array, than creates a new array and put it into the localStorage
function deletItem(id) 
{
	const objectbasket = JSON.parse(localStorage.getItem(project)) || [];	

	for (let count=0; count < objectbasket.length; count++){
	  // delets selected item from array
	  if (objectbasket[count].identifier == id) 
	  {
	    objectbasket.splice(count,1);  
      }
	}
	// restore objects left in localStorage
	objectbasket = JSON.stringify(objectbasket);
	localStorage.setItem(project, objectbasket);
    //localStorage needs some time to store the very first item... so wait a bit for it
    setTimeout(function(){
      showData();
    }, 250);
}	

////////////////////////////
// deletItem() 
// checks onload if item is in objectbasket and checks checkboxes
function checkCheckBoxes(){
  let objectbasket = JSON.parse(localStorage.getItem(project)) || [];	
  for (let count = 0; count < objectbasket.length; count++){
    let checkBox = document.getElementById(objectbasket[count].identifier).children[0].checked = true;
  }
}











