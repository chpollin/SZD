////////////////////////////
////////////////////////////
// databasket
// author: Pollin Christopher 

// GLOBAL VARIABLES
// project = project shortcut like 'szd'
var project = "szd";

////////////////////////////
// getData()
// param: * input_id = id of element with the data- attributes
// Goes through all data- attributes in the element.db_entry and stores them in dbentry (javascript object)
// dbentry is added to the localStorage, which is uniquely by the global project var. 
function add_DB(input_id) 
{
    var databasket = JSON.parse(localStorage.getItem(project)) || [];
    //const dataset = document.getElementById(input_id.closest(".db_entry").id).dataset;  
    const dataset = document.getElementById(input_id).dataset;
    var dbentry = {};
    
    for(var attr in dataset){
        dbentry[attr] = dataset[attr];
    }
    
    databasket.push(dbentry);
    localStorage.setItem(project, JSON.stringify(databasket));
    countEntrys();
 }
 
////////////////////////////
// deletEntryDatabasket() 
// Delets entry in the databasekt using splice() to remove it from the array, than creates a new array and put it into the localStorage
function delet_DB(id) 
{
    // updated databasket
	var databasket = JSON.parse(localStorage.getItem(project));	

	for (var count=0; count < databasket.length; count++){
	console.log(databasket[count].uri);
	  if (databasket[count].uri == id) 
	  {
	    databasket.splice(count,1);  //delets selected entry from array
      }
	}
	
	//Restoring object left into databasket again
	databasket = JSON.stringify(databasket);
	localStorage.setItem(project, databasket);
    location.reload();
}	

////////////////////////////
// calls countEntrys() onload (switching pages etc.)
$(window).on('load', function() {
  countEntrys();
});


////////////////////////////
//	clearData()
//	clears the localStorage if 'Leeren'-Button is pressed
function clearData()
{
	localStorage.clear();
	location.reload();
}

////////////////////////////
//	countEntrys()
// 	called by onLoad();
//	and Datenkorb(n), where n is number of objects in the localStorage
function countEntrys() 
{
	var databasketArray = JSON.parse(localStorage.getItem('szd'));
	if(typeof databasketArray !== 'undefined' && databasketArray.length > 0)
	//databasket is empty
	{
		document.getElementById('db_static').innerHTML = ' ('+ databasketArray.length +')';
	}
}

        
////////////////////////////
//	checkDatabasketStart()
// 	called by onLoad()
//	Goes through the databasket and checks all objects in localStorage if they are in the databasket
function keepCheckboxes() 
{	
	var databasketArray = JSON.parse(localStorage.getItem('szd'));
	var url = window.location.href;

	if(JSON.parse(localStorage.getItem('szd')) != null)
	{
		for (var count = 0; count < databasketArray.length; count++) 
		{
		    var parts = databasketArray[count].uri.split('#');
            var id = parts[parts.length - 1];  //SZDBIB.1249
            var collection = parts[parts.length - 2]; //glossa.uni-graz.at/o:szd.bibliothekskatalog
		   
		    //keepCheckboxes just for all entries at the current site/collection. 
		    if(url.indexOf(collection) !== -1)
		    {
              var currentBox =  document.getElementById('cb'+id);
              currentBox.setAttribute("checked", "true");
              var currentEntry = document.getElementById(id);
              currentEntry.setAttribute("data-check", "checked");
            }
		}	
	}	
}
////////////////////////////
// addItem()
//adds the data from the data property attributs to the entry
function addItem(collection, uri, title, author, signature, location, check) 
{
  var databasketArray = JSON.parse(localStorage.getItem('szd')) || []; 
  var newItem = 
  { 
    "collection" : collection,
	"uri" : uri,
	"title": title,  
	"author": author, 	
	"signature": signature,
	"location": location,
	"check" : check
  } 
  
  //pushs item on a array
  databasketArray.push(newItem);
  //saves entry in the localStorage
  localStorage.setItem('szd', JSON.stringify(databasketArray));
};
////////////////////////////
//	showData()
//
function showData() 
{	
  
	//initalize the localStorage-Array
	var databasketArray = JSON.parse(localStorage['szd']);
	var databasketArrayLength = databasketArray.length;	
    var databasekt_tbody = document.getElementById("databasekt_tbody");

	
	//for every object in the array create a ul = databasketArrayLength 
	for (var outerCount = 0; outerCount < databasketArrayLength; outerCount++) 
	{
		var tr = document.createElement('tr');
		databasekt_tbody.appendChild(tr);
		
		var td_collection = document.createElement('td');
		tr.appendChild(td_collection);
		td_collection.appendChild(document.createTextNode(databasketArray[outerCount].collection));
		
		var td_title = document.createElement('td');
		tr.appendChild(td_title);
		td_title.appendChild(document.createTextNode(databasketArray[outerCount].title));
       
		var td_author = document.createElement('td');
		tr.appendChild(td_author);
		if(databasketArray[outerCount].author)
		  td_author.appendChild(document.createTextNode(databasketArray[outerCount].author));
		
        var uri = databasketArray[outerCount].uri;
		var td_location = document.createElement('td');
		tr.appendChild(td_location);
		//
		td_location.setAttribute("class", 'small');
		if(databasketArray[outerCount].location != ' ')
		{
		  td_location.appendChild(document.createTextNode(databasketArray[outerCount].location + ', ' + databasketArray[outerCount].signature));
		}
		else
		{
		  td_location.appendChild(document.createTextNode(databasketArray[outerCount].signature));
		}
		
		var br = document.createElement('br');
		td_location.appendChild(br);
		var a = document.createElement('a');
		td_location.appendChild(a);
		a.setAttribute("style", "color:#631a34");
		a.setAttribute("title", "Access Object");
		a.setAttribute("href", uri);
		a.appendChild(document.createTextNode(" " + databasketArray[outerCount].uri));
		
		var td_delete = document.createElement('td');
		tr.appendChild(td_delete);
		var button_delet = document.createElement('button');
		button_delet.setAttribute("type", "button");
		button_delet.setAttribute("class", "fas fa-trash btn");
		button_delet.setAttribute("style", "color:#631a34");
		
		button_delet.setAttribute("onclick", "delet_DB('" + uri +"')");
		td_delete.appendChild(button_delet);
    }	
}




