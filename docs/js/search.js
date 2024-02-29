/* get search settings */
var submit_button = d3.select("#submit_button");
submit_button.on("click", runEnter);

function runEnter() {
  /*gather language input*/
  let json_path = retrievePathfromLang();

  /* read manynames.json and filter */
  d3.json(json_path)
    .then(function(data) {
      /*gather user input*/
      let user_input = gatherInput();

      /*filter data*/
      let filtered_data = data.filter(
        fitsSearch(user_input['scope'], user_input['names'],
                  user_input['min_pct'], user_input['max_pct']));

      /*give feedback on search*/
      let filtered_length = filtered_data.length
      searchFeedback(filtered_length);

      /*draw images*/
      //filtered_data = shuffle(filtered_data);
      let img_per_page = 9;  /*9 images per page*/
      const img_gallery = document.getElementById("image_gallery");
      img_gallery.textContent = '';
      display_data = sampleSubset(filtered_data, 0, img_per_page);
      for (let i = 0; i < display_data.length; i++) {
        addImage(display_data[i]['link_mn'], responseStr(display_data[i]['responses']));
      }

      /*image pagination*/
      let btn_page = document.getElementById("current_page");
      btn_page.value = "1"
      let n_gallery_pages = Math.ceil(filtered_length/img_per_page);
      document.getElementById("max_page").innerHTML = `of ${n_gallery_pages.toString()}`;
      let btn_next = document.getElementById("next_page");
      btn_next.disabled = false;
      let btn_prev = document.getElementById("prev_page");
      btn_prev.disabled = false; 
      btn_next.onclick = function(){nextPage(n_gallery_pages, filtered_data, img_per_page)};
      btn_prev.onclick = function(){prevPage(n_gallery_pages, filtered_data, img_per_page)};
      btn_page.addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
          goToPage(n_gallery_pages, filtered_data, img_per_page)
        }
      }
      );

      /*show/hide download buttons*/
      if (filtered_data.length > 0) {
        displayResults('block');
      } else {
        displayResults('none');
      };

      /*add download functionality*/
      let csv_btn = document.getElementById('csv_button')
      csv_btn.onclick = function(){downloadCSV(filtered_data)}
    });
};


/* -------------------------- FUNCTIONS */
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

/*draw images on selected page*/
function drawImages(current_page, filtered_data, img_per_page) {
  const img_gallery = document.getElementById("image_gallery");
  img_gallery.textContent = '';
  first_image = (current_page * img_per_page) - img_per_page
  last_image = first_image + img_per_page
  display_data = sampleSubset(filtered_data, first_image, last_image);
  for (let i = 0; i < display_data.length; i++) {
    addImage(display_data[i]['link_mn'], responseStr(display_data[i]['responses']));
  }
};

/*go to page entered*/
function goToPage(max_pages, filtered_data, img_per_page) {
  let current_page = document.getElementById("current_page").value
  if (isBetween(current_page, 1, max_pages)) {
    changePage(current_page, max_pages);
    drawImages(current_page, filtered_data, img_per_page);
  } else { 
    const img_gallery = document.getElementById("image_gallery");
    changePage(current_page, max_pages);
    img_gallery.style.color = "red";
    img_gallery.textContent = 'Please enter a page number between 1 and ' + max_pages.toString() + '.';
  };
};

/*turn page back*/
function prevPage(max_pages, filtered_data, img_per_page) {

    let current_page = document.getElementById("current_page").value
    if (current_page > 1) {
        current_page--;
        changePage(current_page, max_pages);
      };
    drawImages(current_page, filtered_data, img_per_page);
};

/*turn page forward*/
function nextPage(max_pages, filtered_data, img_per_page){
    let current_page = document.getElementById("current_page").value
    if (current_page < max_pages) {
        current_page++;
        changePage(current_page, max_pages);
    }
    drawImages(current_page, filtered_data, img_per_page);
};

/*change page number, disable buttons if needed*/
function changePage(page, max_pages){
    let btn_next = document.getElementById("next_page");
    let btn_prev = document.getElementById("prev_page");
    let btn_page = document.getElementById("current_page");

    btn_page.value = page;

    if (page === 1) {
        btn_prev.disabled = true;
    } else {
        btn_prev.disabled = false;
    }

    if (page === max_pages) {
        btn_next.disabled = true;
    } else {
        btn_next.disabled = false;
    }

    if (!isBetween(page, 1, max_pages)) {
      btn_next.disabled = true;
      btn_prev.disabled = true;
    } 
};

/*shuffle array*/
function shuffle(array) {
  const shuffled_array = [...array].sort(() => 0.5 - Math.random());
  return shuffled_array;
};

/* convert to csv and start download*/
function downloadCSV(filtered_data) {
  document.getElementById('csv_button').disabled = true;
  makeCSV(filtered_data)
  .then(function(csv_dat) {
    const blob = new Blob([csv_dat], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const csv_download_link = document.createElement("a")
    csv_download_link.setAttribute('href', url);
    csv_download_link.setAttribute('download', 'ManyNames_data.csv');
    document.body.appendChild(csv_download_link)
    csv_download_link.click();
    document.body.removeChild(csv_download_link);
    window.URL.revokeObjectURL(url)
    document.getElementById('csv_button').disabled = false;
  });
};

/*helper function to reshape data into csv string*/
function makeCSV(data_obj) {
  return new Promise(function(resolve, reject){
    /*variable names*/
    let img_vars = ['vg_image_id', 'vg_object_id', 'link_mn', 'link_vg', 'total_responses'];
    let name_vars = ['name', 'is_topname', 'name_proportion'];

    /*reshape to flatten input data*/
    let dat_flat = [];
    for (dat_in of data_obj) {
        let dat_row = {};
        for (k of img_vars) {
          dat_row[k] = dat_in[k];
        }
        for (const [nam,cnt] of Object.entries(dat_in['responses'])) {
          dat_row['name'] = nam;
          dat_row['isTopname'] = nam === dat_in['topname'];
          dat_row['response_count'] = cnt;
          dat_flat.push({...dat_row});
        };
    };

    let csv_rows = [];
    const header = Object.keys(dat_flat[0])
    csv_rows.push(header.join(','));
    for (row of dat_flat) {
      const vals = Object.values(row).join(',');
      csv_rows.push(vals.concat())
    }
    resolve(csv_rows.join('\n'));
  });
};

/*add download buttons*/
function displayResults(display_style) {
  let csv_download_div = document.getElementById("csv_download")
  // let zip_download_div = document.getElementById("zip_download")
  let images_div = document.getElementById("images")
  csv_download_div.style.display = display_style
  // zip_download_div.style.display = display_style
  images_div.style.display = display_style
};

/* give search feedback*/
function searchFeedback(n_results) {
  var search_feedback = document.getElementById("search_feedback")
  if (n_results > 0) {
    search_feedback.className = 'text-success';
    search_feedback.innerHTML = n_results.toString() + ' images fit your search criteria.' + 'You can download the corresponding naming data (in csv-format). The <a href="./download.html">download</a> section contains scripts to download the images in your search result based on this csv.';
    if (n_results === 1) {
      search_feedback.innerHTML.replace('images fit', 'image fits');
    };
  } else if (n_results === 0) {
    search_feedback.className = 'text-danger';
    search_feedback.innerHTML = 'No images fit your search criteria. Please make sure that you have set a sensible range for name agreement. Please also consider other spelling variants of the names you are looking for. You can browse the list of all names (and their spelling) found in ManyNames  <a href="./names.html">here</a>.';
  };
};

/* add image to gallery*/
function addImage(img_url, resp_string) {
  let img_url_small = img_url.replace('.png', '_s.png')
  img_url_small = img_url_small.replace('http://manynames.upf.edu//', 'http://manynames.upf.edu//small//') // set to thumbnail path
  var img_gallery = document.getElementById("image_gallery");
  var img_div = document.createElement('div');
  img_div.className = 'col-lg-3 col-md-4 col-8 m-1 rounded'
  img_div.setAttribute('title', resp_string);
  img_div.style.backgroundColor = 'WhiteSmoke';
  var thumbnail = document.createElement('a');
  thumbnail.className = 'd-block h-100';
  thumbnail.setAttribute('href', img_url);
  thumbnail.setAttribute('target', '_blank');
  var figure = document.createElement('figure');
  figure.className = 'figure mt-2';
  var img = document.createElement("img");
  img.className = "img-fluid";
  img.setAttribute("src", img_url_small); // set to img_url_small for thumbnails
  img.setAttribute("alt", "");
  img.style.maxHeight = '80%';
  var caption = document.createElement("figcaption");
  caption.className = "figure-caption text-center"
  caption.innerHTML = resp_string;
  figure.appendChild(img);
  figure.appendChild(caption);
  thumbnail.appendChild(figure);
  img_div.appendChild(thumbnail);
  img_gallery.appendChild(img_div);
};

/* response object to string*/
function responseStr(obj){
  resp_string = '';
  for (const [nam, cnt] of Object.entries(obj)) {
      resp_string += `${nam} (${cnt}), `;
    }
  return resp_string.slice(0,-2);
};

/*gather input*/
function gatherInput() {
  /*retrieve language*/
  var lang = document.getElementById('dropdownMenuButton').innerText;
  /*scope setting*/
  var all_nam_button = document.getElementById("all_nam_button")['checked'];
  var any_nam_button = document.getElementById("any_nam_button")['checked'];
  var any_top_button = document.getElementById("any_top_button")['checked'];
  if (all_nam_button) {var scope = 'all_nam'}
  else if (any_nam_button) {var scope = 'any_nam'}
  else if (any_top_button) {var scope = 'any_top'}

  /*names*/
  /*remove leading and trailing spaces, remove anything else that is not a letter or space */
  var names_input = document.getElementById("names_field")['value'];
  if (names_input === "") {
    var names_input = document.getElementById("names_field").placeholder;
  }

  if (lang === 'Chinese') {
    var names = names_input.split('，');
  } else {
    var names = names_input.split(',');
  }

  if (lang === 'English') {
    names.forEach(function(val, idx) {
      names[idx] = val.trim().replace(/[^a-zA-Z\- ]/g, "");
    })
  }
  else if (lang === 'Chinese') {
    names.forEach(function(val, idx) {
      names[idx] = val.trim().replace(/[^\u4E00-\u9FFF ]/g, "");
    })
  }

  var names = names.filter(Boolean)

  /*min pct*/
  var min_pct = document.getElementById("min_pct_field")['value'];
  if (min_pct === "") {
    var min_pct = document.getElementById("min_pct_field").placeholder;
  }
  var min_pct = min_pct / 100

  /*max pct*/
  var max_pct = document.getElementById("max_pct_field")['value'];
  if (max_pct === "") {
    var max_pct = document.getElementById("max_pct_field").placeholder;
  }
  var max_pct = max_pct / 100

  /*return as object*/
  let user_input = {scope: scope, names:names, min_pct:min_pct, max_pct:max_pct}
  return user_input
};

/* sample subset of data (to display) */
function sampleSubset(arr, first, last) {
  return arr.slice(first, last);
};

/* check if percentage in range */
function isBetween(x, min, max) {
  return x >= min && x <= max;
};

/* check search criteria for name and response percent pair */
function responseFits(resp, pct, names, min_pct, max_pct) {
  if (typeof resp === 'string') {
    return names.includes(resp) && isBetween(pct, min_pct, max_pct);
  } else if (typeof resp === 'object') {
    var checked = []
    for (const r of resp) {
      checked.push(names.includes(r) && isBetween(pct, min_pct, max_pct));
    }
    return(checked.some(Boolean))
  }
};

/* filter function (for now only one topname and "any_topname") */
function fitsSearch(scope, names, min_pct, max_pct) {
  return function(el) {
    if (scope === 'any_top') {
      return responseFits(el.topname, el.perc_top, names, min_pct, max_pct);
    } else if (scope === 'any_nam'){
      var checked = []
      for (const resp of Object.entries(el['responses'])) {
          checked.push(responseFits(resp[0], resp[1]/el['total_responses'],
                       names, min_pct, max_pct));
        }
      return(checked.some(Boolean))
    } else if (scope === 'all_nam'){
      responses = Object.keys(el['responses'])
      var chkNams = names.every(nam => responses.includes(nam));
      if (!chkNams) {
        var checked = [false]
      } else {
        var checked = []
        for (const resp of Object.entries(el['responses'])) {
            if (names.includes(resp[0])) {
              checked.push(responseFits(resp[0], resp[1]/el['total_responses'],
                           names, min_pct, max_pct));
            };
        }
      }
      return(checked.every(Boolean));
    };
  };
};
