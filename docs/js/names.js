createTable()

function createTable() {
  // clear the content inside the <tbody> element to prevent from adding one table to another instead of creating a new one
  let tbody = document.querySelector("#names_table tbody");
  tbody.innerHTML = '';

  // specify the path of the JSON file depending on the selected language
  let json_path = retrievePathfromLang();

  // read manynames.json and filter
  d3.json(json_path)

// extract names and counts from data
  .then(function(data) {
    let name_data = extractNameDat(data);
    name_data = Object.keys(name_data).sort().reduce(
      (obj, key) => { 
        obj[key] = name_data[key]; 
        return obj;
      }, 
      {}
    );
    return addCoocurrence(data, name_data);
  })

  // setup full table
  .then(function(name_data){

    let names_table = document.getElementById("names_table");
    name_data.reverse();
    for (const [name, ndata] of name_data) {
      addRow(name, ndata, names_table);
    };
    updateTable();
    names_table.style.display = "table";
  })
};


// -------------------------- FUNCTIONS
/*select JSON file depending on language*/
function retrievePathfromLang() {
  var lang_button = document.getElementById('dropdownMenuButton').innerText;

  switch(lang_button) {
    case 'English':
      path = "https://raw.githubusercontent.com/amore-upf/manynames/master/other-data/manynames-en.json";
      break;
    case 'Chinese':
      path = "https://raw.githubusercontent.com/amore-upf/manynames/master/other-data/manynames-zh.json";
      break;
  }
  return path
};

// extract names and counts from manynames data
function extractNameDat(data) {
  // Check current language
  var lang_button = document.getElementById('dropdownMenuButton').innerText;
  // Create empty object
  const name_data = {};
  // Iterate through each element of the MN JSON
  data.forEach(element => {
    if (lang_button === 'English') {
        // Iterate through each object in key 'responses' (=column 'responses')
        Object.entries(element.responses).forEach(([key, value]) => {
          if (name_data.hasOwnProperty(key) && element.topname === key) {
            name_data[key].overall += value;
            name_data[key].img_any += 1;
            name_data[key].img_top += 1;
          } else if (name_data.hasOwnProperty(key) && element.topname != key) {
            name_data[key].overall += value;
            name_data[key].img_any += 1;
          } else if (!name_data.hasOwnProperty(key) && element.topname === key) {
            name_data[key] = {overall: value, img_any: 1, img_top: 1};
          } else {
            name_data[key] = {overall: value, img_any: 1, img_top: 0};
          }
        });
      } else if (lang_button === 'Chinese') {
        Object.entries(element.responses).forEach(([key, value]) => {
          if (name_data.hasOwnProperty(key) && element.topname.includes(key)) {
            name_data[key].overall += value;
            name_data[key].img_any += 1;
            name_data[key].img_top += 1;
          } else if (name_data.hasOwnProperty(key) && (element.topname.includes(key) == false)) {
            name_data[key].overall += value;
            name_data[key].img_any += 1;
          } else if (!name_data.hasOwnProperty(key) && element.topname.includes(key)) {
            name_data[key] = {overall: value, img_any: 1, img_top: 1};
          } else {
            name_data[key] = {overall: value, img_any: 1, img_top: 0};
          }
        });
      }
    });
    return name_data;
  };

// add co-occurence
function addCoocurrence(data, name_data){
  Object.keys(name_data).forEach(key => {
    name_data[key].coocurrence = new Set()});
  data.forEach(element => {
    Object.keys(element.responses).forEach((key) => {
      Object.keys(element.responses).forEach(itm => name_data[key].coocurrence.add(itm));
    })
  });
  return Object.entries(name_data);
};

// add table rows
function addRow(name, name_data, table) {
  let row = table.getElementsByTagName('tbody')[0].insertRow(0);
  row.style.display = 'table-row';
  row.dataset.name = name;
  row.dataset.isTop = name_data.img_top > 0;
  let cell_name = row.insertCell(0);
  let cell_total = row.insertCell(1);
  let cell_any = row.insertCell(2);
  let cell_top = row.insertCell(3);
  let cell_cooc = row.insertCell(4);
  cell_name.innerHTML = name;
  cell_total.innerHTML = name_data.overall;
  cell_any.innerHTML = name_data.img_any;
  cell_top.innerHTML = name_data.img_top;
  let cooc = Array.from(name_data.coocurrence).sort();
  cooc.splice(cooc.indexOf(name), 1); // remove name from its own coocurrence set
  cell_cooc.innerHTML = cooc.join(', ');
  cell_total.style.textAlign = 'center';
  cell_any.style.textAlign = 'center';
  cell_top.style.textAlign = 'center';
};

//function to update table with user input
function updateTable() {
  var lang = document.getElementById('dropdownMenuButton').innerText;
  //gather all rows
  let all_rows = names_table.querySelectorAll("tr[data-name]");

  //get text input, trim spaces split words
  var names_input = document.getElementById("names_field")['value'];
  
  if (names_input === "") {
    var names_input = document.getElementById("names_field").placeholder;
  }

  if (lang === 'Chinese') {
    var names = names_input.split('，'); // The exact word(s) the user is searching for
  } else {
    var names = names_input.split(',');
  }

  if (lang === 'English') {
    names.forEach(function(val, idx) {
      names[idx] = val.trim().replace(/[^a-zA-Z\- ]/g, ""); // !!!!!! only keep alphabetical characters, spaces, and hyphens
    })
  }
  else if (lang === 'Chinese') {
    names.forEach(function(val, idx) {
      names[idx] = val.trim().replace(/[^\u4E00-\u9FFF ]/g, "");
    })
  }
  
  names = names.filter(Boolean);

  //filter by name
  for (let i = 0; i < all_rows.length; i++) {
    if (names.length === 0) {
      all_rows[i].style.display = "table-row";
    } else {
      let row_name = all_rows[i].getAttribute('data-name');
      if (!names.filter(el => row_name.includes(el)).length > 0) {
        all_rows[i].style.display = "none"
      } else {
        all_rows[i].style.display = "table-row"
      };

    };
  };

  //filter by topname status
  if (document.getElementById("topname_button").checked) {
    let nontop_rows = Array.from(all_rows).filter(el => el.dataset.isTop === "false")
    for (let i = 0; i < nontop_rows.length; i++) {
      nontop_rows[i].style.display = "none";
    };
  }; 
};
