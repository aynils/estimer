const CITIES_PRICING_PATH = '/agence/pricing/'

const DEPARTEMENTS = [
    {
        "code": "00",
        "name": "Département"
    },
    {
        "code": "62",
        "name": "Pas-de-Calais"
    },
    {
        "code": "38",
        "name": "Isère"
    },
    {
        "code": "34",
        "name": "Hérault"
    }
]

function citySearch() {
    return {
        selectedCity: "",
        selectedDepartement: "00",
        cities: JSON.parse(document.getElementById('cities_pricing').textContent),
        departements: DEPARTEMENTS,
        selectedCities: [],
        price ()  {
            return  this.selectedCities.reduce((total, city) => {
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
