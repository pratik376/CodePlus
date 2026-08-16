def run_impact_analysis(graph):
    while True:
        file_name = input(
            "\nFile for impact analysis (or 'exit'): "
        ).strip()

        if file_name.lower() == "exit":
            break

        if not file_name:
            continue

        impacted = graph.impact_analysis(file_name)

        if not impacted:
            print("No dependent files found.")
            continue

        production_files = []
        test_files = []

        for file in impacted:
            normalized = file.replace("\\", "/")

            if (
                "/tests/" in normalized
                or normalized.startswith("tests/")
                or normalized.split("/")[-1].startswith("test_")
            ):
                test_files.append(file)
            else:
                production_files.append(file)

        print("\nPRODUCTION IMPACT")
        print("-" * 40)

        if production_files:
            for file in sorted(production_files):
                print(f"  <- {file}")
        else:
            print("  None")

        print("\nAFFECTED TESTS")
        print("-" * 40)

        if test_files:
            for file in sorted(test_files):
                print(f"  <- {file}")
        else:
            print("  None")