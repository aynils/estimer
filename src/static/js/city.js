const IRIS_DATA_PATH = '/iris/data/'

function irisData() {
    return {
        irisData: {
            iris_name: city_name,
            price_evolution_text: price_evolution_text.replace("&#x27;","'"),
            chart_b64_svg: chart_b64_svg,
        },
    };
}


function selectIris(event) {
    const IRISCode = event.target.value
    const url = new URL(IRIS_DATA_PATH, document.location)
    url.searchParams.append("iris", IRISCode);
    fetch(url, {method: "GET"})
        .then(result => result.json())
        .then(json => {
            console.log('result', json)
            this.irisData = json
        })

}
