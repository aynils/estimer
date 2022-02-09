const IRIS_DATA_PATH = '/iris/data'

async function selectIris() {
    return {
        irisData: {},
        async selectIris (IRISCode) {
            const url = new URL(IRIS_DATA_PATH)
            const queryParams = {"iris":IRISCode}
            for (let key in queryParams) { url.searchParams.append(key, data[key]); }
            const result = await fetch(url);
            if (result.ok){
                console.log('result', result)
                this.irisData = {foo: "bar"}
            }
         }

    };
}
