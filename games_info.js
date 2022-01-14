// ============================= TO GO TO PAGE ============================= //
// OPEN CHROME AND PRESS F12 TO OPEN DEVTOOLS
// To go to the scrape page use code bellow

const PAGE = 1
const SYSTEM = 'genesis'
const URL_STR = `https://www.emu-land.net/consoles/${SYSTEM}/roms/top/${PAGE}`

window.location.href = URL_STR

// ============================= ON LIST PAGE ============================= //

// ON GAMES LIST PAGE
// After you are on the page use code bellow to scrape games data

let games_data = []

let games_list = document.querySelectorAll('.fcontainer')
let games_array = Array.from(games_list)


/*
* Thanks *
Thanks to codeguy for this slugify. 
Old but still good enough for this tools.
*/

function slugify (str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();
  
    // remove accents, swap ñ for n, etc
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    var to   = "aaaaeeeeiiiioooouuuunc------";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    return str;
}

function scrape_games_data() {
    games_array.forEach(el => {
        scrap_one_game(el)
    });

    console.log("[INFO] GAMES DATA: ", games_data);
}

function scrap_one_game(game_dom) {
    let game_object = {
        "name": '',         //+
        "slug": '',         //+
        "genres": null,     //+
        "rate": '',         //+
        "players": '1',      //+
        "downloads": 0,     //+
        "size": '',         //+
        "picture": null     //+
    };

    let name = game_dom.querySelector('.fheader') ? game_dom.querySelector('.fheader').innerText.trim() : '';
    let slug = slugify(name);
    let genres = game_dom.querySelectorAll('.finfo')[0] ? game_dom.querySelectorAll('.finfo')[0].innerText.replace("Жанр: ", "").split(',') : '';
    let players = game_dom.querySelectorAll('.finfo')[1] ? game_dom.querySelectorAll('.finfo')[1].innerText.replace("Игроки: ", "") : '';
    let description = game_dom.querySelector('span[id]') ? game_dom.querySelector('span[id]').innerText.split('\n')[0] : '';
    let rate = game_dom.querySelector('.rating_info') ? game_dom.querySelector('.rating_info').querySelector('span[id]').innerText + '/10' : '0/10';
    let size = game_dom.querySelector('.fbottom') ? game_dom.querySelector('.fbottom').innerText.split('|')[0].replace('Размер:', '').trim() : '';
    let downloads = game_dom.querySelector('.fbottom') ? +game_dom.querySelector('.fbottom').innerText.split('|')[1].replace('Загрузок:', '').trim() : 0;
    let picture = game_dom.querySelector('.ftext') ? game_dom.querySelector('.ftext').querySelector('img').src : null;

    console.log("[INFO] SCRAPING GAME: ", name);


    game_object.name = name;
    game_object.slug = slug;
    game_object.genres = genres;
    game_object.players = players;
    game_object.description = description;
    game_object.rate = rate;
    game_object.size = size;
    game_object.downloads = downloads;
    game_object.picture = picture;

    games_data.push(game_object);
}

function init() {
    console.log("[INFO] START SCRAPING | NORMAL START");
    try {
        scrape_games_data();
    } catch( error ) {
        console.log("[WARNING] EXCEPTION CAUGHT. STOP SCRAPING PROCCESS. | ", error);
    }
    console.log("[INFO] STOP SCRAPING | NORMAL STOP");
}

init();