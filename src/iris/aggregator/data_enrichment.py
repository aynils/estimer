from src.dvf.data.cities import get_simple_sales, get_cities, ONE_YEAR_AGO, add_iris_to_mutations
import pandas as pd
from django.conf import settings

import warnings

from django.core.cache import CacheKeyWarning

warnings.simplefilter("ignore", CacheKeyWarning)


def create_mutation_iris_relation(request):
    all_mutations = pd.DataFrame()
    communes = get_cities()
    for index, commune in enumerate(communes):
        print(f"----Getting mutations for {commune.nom_commune}...")
        mutations = get_simple_sales(
            code_commune=commune.code_commune, types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        if mutations.empty:
            print(f"----No mutation from {ONE_YEAR_AGO} for {commune.nom_commune} ({commune.code_commune})")
            continue
        print(f"----Adding mutations for {commune.nom_commune}...")
        mutations = add_iris_to_mutations(code_commune=commune.code_commune, mutations=mutations)
        all_mutations = all_mutations.append(mutations, ignore_index=True)
        print(f"{index + 1}/{len(communes)} -  {commune.nom_commune} ({commune.code_commune}) DONE")

    ids = all_mutations[["code_iris", "id_mutation"]]
    ids.to_csv(f"{settings.BASE_DIR}/code_iris_mutation_id_relation.csv", index=False)
    print("Done")
    return ""
