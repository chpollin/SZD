////////////////////////////
////////////////////////////
// databasket
// author: Pollin Christopher 

// GLOBAL VARIABLES
// project = project shortcut like 'szd' or 'depcha'
var project = "szd";

////////////////////////////
// getData()
// param: * input_id = id of element with the data- attributes
// Goes through all data- attributes in the element.db_entry and stores them in dbentry (javascript object)
// dbentry is added to the localStorage, which is uniquely by the global project var. 
function add_DB(input_id) 
{
    var databasket = JSON.parse(localStorage.getItem(project)) || [];
    const dataset = document.getElementById(input_id.closest(".db_entry").id).dataset;    
    var dbentry = {};

    for(var attr in dataset){
        dbentry[attr] = dataset[attr];
    }
    databasket.push(dbentry);
    localStorage.setItem(project, JSON.stringify(databasket));
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
	var datenkorbArray = JSON.parse(localStorage.getItem('szd'));
	
	if(typeof datenkorbArray !== 'undefined' && datenkorbArray.length > 0)
	//databasket is empty
	{
		document.getElementById('databasket_static').innerHTML = ' ('+ datenkorbArray.length +')';
	}
}

////////////////////////////
//	clear()
// 	called by onLoad();
function clear() 
		{
          document.getElementById("datenkorb_static").innerHTML = "";
        }	
////////////////////////////
//	checkDatabasketStart()
// 	called by onLoad()
//	Goes through the databasket and checks all objects in localStorage if they are in the databasket
function keepCheckboxes() 
{	
	var datenkorbArray = JSON.parse(localStorage.getItem('szd'));
	var url = window.location.href;

	if(JSON.parse(localStorage.getItem('szd')) != null)
	{
		for (var count = 0; count < datenkorbArray.length; count++) 
		{
		    var parts = datenkorbArray[count].uri.split('#');
            var id = parts[parts.length - 1];  //SZDBIB.1249
            var collection = parts[parts.length - 2]; //glossa.uni-graz.at/o:szd.bibliothekskatalog
		   
		    //keepCheckboxes just for all entries at the actual site/collection. 
		    if(url.indexOf(collection) !== -1)
		    {
              var actualBox =  document.getElementById('cb'+id);
              actualBox.setAttribute("checked", "true");
              var actualEntry = document.getElementById(id);
              actualEntry.setAttribute("data-check", "checked");
            }
		}	
	}	
}
////////////////////////////
// addItem()
//adds the data from the data property attributs to the entry
function addItem(uri, title, author, date, involved, check) 
{
  var datenkorbArray = JSON.parse(localStorage.getItem('szd')) || []; 
  var newItem = 
  { 
	"uri" : uri,
	"title": title,  
	"author": author, 	
	"date": date,
	"involved": involved,
	"check" : check
  } 
  
  //pushs item on a array
  datenkorbArray.push(newItem);
  //saves entry in the localStorage
  localStorage.setItem('szd', JSON.stringify(datenkorbArray));
};
////////////////////////////
//	showData()
//
function showData() 
{	
  
	//initalize the localStorage-Array
	var datenkorbArray = JSON.parse(localStorage['szd']);
	var datenkorbArrayLength = datenkorbArray.length;	
    var databasekt_tbody = document.getElementById("databasekt_tbody");

    

	
	//for every object in the array create a ul = datenkorbArrayLength 
	for (var outerCount = 0; outerCount < datenkorbArrayLength; outerCount++) 
	{
		var tr = document.createElement('tr');
		databasekt_tbody.appendChild(tr);
		
		var td_title = document.createElement('td');
		tr.appendChild(td_title);
		
		var a = document.createElement('a');
        var uri = datenkorbArray[outerCount].uri;
        
		a.setAttribute("style", "color:#631a34");
		a.setAttribute("title", "Access Object");
		a.setAttribute("href", uri);
		a.setAttribute("onclick", "scrolldown(this)");
	    td_title.appendChild(a)
		a.appendChild(document.createTextNode(datenkorbArray[outerCount].title));

      	
		var td_author = document.createElement('td');
		tr.appendChild(td_author);
		if(datenkorbArray[outerCount].author)
		  td_author.appendChild(document.createTextNode(datenkorbArray[outerCount].author));
		
		var td_involved = document.createElement('td');
		tr.appendChild(td_involved);
		if(datenkorbArray[outerCount].involved)
		  td_involved.appendChild(document.createTextNode(datenkorbArray[outerCount].involved));

		var td_date = document.createElement('td');
		tr.appendChild(td_date);
		if(datenkorbArray[outerCount].date)
		  td_date.appendChild(document.createTextNode(datenkorbArray[outerCount].date));
		

		var td_delete = document.createElement('td');
		tr.appendChild(td_delete);
		var button_delet = document.createElement('button');
		button_delet.setAttribute("type", "button");
		button_delet.setAttribute("class", "fas fa-ban");
		button_delet.setAttribute("onclick", "delet_DB('" + uri +"')");
		td_delete.appendChild(button_delet);
    }	
}


////////////////////////////
////////////////////////////
//
function printDatabasket() 
{
    var doc = new jsPDF();
    var specialElementHandlers = {
    '#editor': function (element, renderer) 
    {
        return true;
    }
};

$('#cmd').click(function () {
    doc.fromHTML($('#content').html(), 15, 15, {
        'width': 170,
            'elementHandlers': specialElementHandlers
    });
    doc.save('sample-file.pdf');
});
}

/*$(window).on('load', function() {
  countEntrys();
});*/

