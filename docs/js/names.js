// read manynames.json and filter
d3.json("https://raw.githubusercontent.com/amore-upf/manynames/master/manynames.json")

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


// -------------------------- FUNCTIONS
// extract names and counts from manynames data
function extractNameDat(data) {
  const name_data = {};
  data.forEach(element => {
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

  //gather all rows
  let all_rows = names_table.querySelectorAll("tr[data-name]");

  //get text input, trim spaces split words
  var names_input = document.getElementById("names_field")['value'];
  
  if (names_input === "") {
    var names_input = document.getElementById("names_field").placeholder;
  }

  names = names_input.split(',')
  names.forEach(function(val, idx) {
    names[idx] = val.trim().replace(/[^a-zA-Z ]/g, "");
  })
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
