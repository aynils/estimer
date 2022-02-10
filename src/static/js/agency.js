function citySearch()
        {
            return {
                selectedCity: "",
                cities: JSON.parse(document.getElementById('cities_pricing').textContent),
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
