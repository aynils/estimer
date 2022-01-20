function citySearch()
        {
            return {
                selectedCity: "",
                cities: [{id : 100, price : 25, name: "Montpellier", zipcode: 34000},{id : 15, price : 25, name: "Testouille", zipcode: 38090},{id : 88, price : 25, name: "Test", zipcode: 34800}],
                selectedCities: [],
                addCities()
                {
                    const id = parseInt(this.selectedCity);
                    const city = this.cities.find(city => id === city.id);
                    this.selectedCities.push(city);
                    this.selectedCity = "";
                    this.cities = this.cities.map(city => {
                        if(city.id === id)
                        {
                            city.disabled = true;
                        }
                        return city;
                    });
                },
                deleteCities(id)
                {
                    this.selectedCities = this.selectedCities.filter((city) => {
                        return id !== city.id
                    })
                    this.cities = this.cities.map(city => {
                        if(city.id === id)
                        {
                            city.disabled = false;
                        }
                        return city;
                    });
                },

            };
        }
