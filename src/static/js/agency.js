const CITIES_PRICING_PATH = '/agence/pricing/'

const DEPARTEMENTS = [
    {
        "code": "00",
        "name": "Département"
    },

    {
        "code": "01",
        "name": "Ain"
    },
    {
        "code": "02",
        "name": "Aisne"
    },
    {
        "code": "03",
        "name": "Allier"
    },
    {
        "code": "04",
        "name": "Alpes-de-Haute-Provence"
    },
    {
        "code": "05",
        "name": "Hautes-alpes"
    },
    {
        "code": "06",
        "name": "Alpes-maritimes"
    },
    {
        "code": "07",
        "name": "Aisne"
    },
    {
        "code": "08",
        "name": "Aisne"
    },
    {
        "code": "09",
        "name": "Ariège"
    },
    {
        "code": "10",
        "name": "Aube"
    },
    {
        "code": "11",
        "name": "Aude"
    },
    {
        "code": "12",
        "name": "Aveyron"
    },
    {
        "code": "13",
        "name": "Bouches-du-Rhône"
    },
    {
        "code": "14",
        "name": "Calvados"
    },
    {
        "code": "15",
        "name": "Cantal"
    },
    {
        "code": "16",
        "name": "Charente"
    },
    {
        "code": "17",
        "name": "Charente-maritime"
    },
    {
        "code": "18",
        "name": "Cher"
    },
    {
        "code": "19",
        "name": "Corrèze"
    },
    {
        "code": "2A",
        "name": "Corse-du-sud"
    },
    {
        "code": "2B",
        "name": "Haute-Corse"
    },
    {
        "code": "21",
        "name": "Côte-d'Or"
    },
    {
        "code": "22",
        "name": "Côtes-d'Armor"
    },
    {
        "code": "23",
        "name": "Creuse"
    },
    {
        "code": "24",
        "name": "Dordogne"
    },
    {
        "code": "25",
        "name": "Doubs"
    },
    {
        "code": "26",
        "name": "Drôme"
    },
    {
        "code": "27",
        "name": "Eure"
    },
    {
        "code": "28",
        "name": "Eure-et-loir"
    },
    {
        "code": "29",
        "name": "Finistère"
    },
    {
        "code": "30",
        "name": "Gard"
    },
    {
        "code": "31",
        "name": "Haute-garonne"
    },
    {
        "code": "32",
        "name": "Gers"
    },
    {
        "code": "33",
        "name": "Gironde"
    },
    {
        "code": "34",
        "name": "Hérault"
    },
    {
        "code": "35",
        "name": "Ille-et-vilaine"
    },
    {
        "code": "36",
        "name": "Indre"
    },
    {
        "code": "37",
        "name": "Indre-et-loire"
    },
    {
        "code": "38",
        "name": "Isère"
    },
    {
        "code": "39",
        "name": "Jura"
    },
    {
        "code": "40",
        "name": "Landes"
    },
    {
        "code": "41",
        "name": "Loir-et-cher"
    },
    {
        "code": "42",
        "name": "Loire"
    },
    {
        "code": "43",
        "name": "Haute-loire"
    },
    {
        "code": "44",
        "name": "Loire-atlantique"
    },
    {
        "code": "45",
        "name": "Loiret"
    },
    {
        "code": "46",
        "name": "Lot"
    },
    {
        "code": "47",
        "name": "Lot-et-garonne"
    },
    {
        "code": "48",
        "name": "Lozère"
    },
    {
        "code": "49",
        "name": "Maine-et-loire"
    },
    {
        "code": "50",
        "name": "Manche"
    },
    {
        "code": "51",
        "name": "Marne"
    },
    {
        "code": "52",
        "name": "Haute-marne"
    },
    {
        "code": "53",
        "name": "Mayenne"
    },
    {
        "code": "54",
        "name": "Meurthe-et-moselle"
    },
    {
        "code": "55",
        "name": "Meuse"
    },
    {
        "code": "56",
        "name": "Morbihan"
    },
    {
        "code": "57",
        "name": "Moselle"
    },
    {
        "code": "58",
        "name": "Nièvre"
    },
    {
        "code": "59",
        "name": "Nord"
    },
    {
        "code": "60",
        "name": "Oise"
    },
    {
        "code": "61",
        "name": "Orne"
    },
    {
        "code": "62",
        "name": "Pas-de-calais"
    },
    {
        "code": "63",
        "name": "Puy-de-dôme"
    },
    {
        "code": "64",
        "name": "Pyrénées-atlantiques"
    },
    {
        "code": "65",
        "name": "Hautes-Pyrénées"
    },
    {
        "code": "66",
        "name": "Pyrénées-orientales"
    },
    {
        "code": "67",
        "name": "Bas-rhin"
    },
    {
        "code": "68",
        "name": "Haut-rhin"
    },
    {
        "code": "69",
        "name": "Rhône"
    },
    {
        "code": "70",
        "name": "Haute-saône"
    },
    {
        "code": "71",
        "name": "Saône-et-loire"
    },
    {
        "code": "72",
        "name": "Sarthe"
    },
    {
        "code": "73",
        "name": "Savoie"
    },
    {
        "code": "74",
        "name": "Haute-savoie"
    },
    {
        "code": "75",
        "name": "Paris"
    },
    {
        "code": "76",
        "name": "Seine-maritime"
    },
    {
        "code": "77",
        "name": "Seine-et-marne"
    },
    {
        "code": "78",
        "name": "Yvelines"
    },
    {
        "code": "79",
        "name": "Deux-sèvres"
    },
    {
        "code": "80",
        "name": "Somme"
    },
    {
        "code": "81",
        "name": "Tarn"
    },
    {
        "code": "82",
        "name": "Tarn-et-Garonne"
    },
    {
        "code": "83",
        "name": "Var"
    },
    {
        "code": "84",
        "name": "Vaucluse"
    },
    {
        "code": "85",
        "name": "Vendée"
    },
    {
        "code": "86",
        "name": "Vienne"
    },
    {
        "code": "87",
        "name": "Haute-vienne"
    },
    {
        "code": "88",
        "name": "Vosges"
    },
    {
        "code": "89",
        "name": "Yonne"
    },
    {
        "code": "90",
        "name": "Territoire de belfort"
    },
    {
        "code": "91",
        "name": "Essonne"
    },
    {
        "code": "92",
        "name": "Hauts-de-seine"
    },
    {
        "code": "93",
        "name": "Seine-Saint-Denis"
    },
    {
        "code": "94",
        "name": "Val-de-marne"
    },
    {
        "code": "95",
        "name": "Val-d'Oise"
    },
    {
        "code": "971",
        "name": "Guadeloupe"
    },
    {
        "code": "972",
        "name": "Martinique"
    },
    {
        "code": "973",
        "name": "Guyane"
    },
    {
        "code": "974",
        "name": "La réunion"
    },
    {
        "code": "976",
        "name": "Mayotte"
    }
]


function citySearch() {
    return {
        selectedCity: "",
        selectedDepartement: "00",
        cities: JSON.parse(document.getElementById('cities_pricing').textContent),
        departements: DEPARTEMENTS,
        selectedCities: [],
        price() {
            return this.selectedCities.reduce((total, city) => {
                return total + city.price
            }, 0)
        },
        addCities() {
            const id = parseInt(this.selectedCity);
            const city = this.cities.find(city => id === city.id);
            this.selectedCities.push(city);
            this.selectedCity = "";
            this.cities = this.cities.map(city => {
                if (city.id === id) {
                    city.disabled = true;
                }
                return city;
            });
        },
        deleteCities(id) {
            this.selectedCities = this.selectedCities.filter((city) => {
                return id !== city.id
            })
            this.cities = this.cities.map(city => {
                if (city.id === id) {
                    city.disabled = false;
                }
                return city;
            });
        },
        mailto() {
            const formattedBody = `Bonjour Olivier, \n\nJe souhaiterais obtenir l'exclusivité sur les communes suivantes : \n${this.selectedCities.map(city => `  - ${city.name} (${city.zipcode})`).join('\n')}\n\n Bien à vous,\n`
            const formattedSubject = `Je voudrais l'exclusivité sur ces communes.`
            return "mailto:contact@estimer.com?subject=" + formattedSubject + "&body=" + encodeURIComponent(formattedBody);
        }

    };
}


function selectDepartement(event) {
    const codeDepartement = event.target.value
    const url = new URL(CITIES_PRICING_PATH, document.location)
    url.searchParams.append("code_departement", codeDepartement);
    fetch(url, {method: "GET"})
        .then(result => result.json())
        .then(json => {
            console.log('result', json)
            this.cities = json.cities_pricing
            this.departements = DEPARTEMENTS
            this.selectedDepartement = codeDepartement
        })

}
