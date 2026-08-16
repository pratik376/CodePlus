from graph.parser import PythonDependencyParser


def print_dependencies(graph):
    print("\nDIRECT DEPENDENCIES")
    print("=" * 60)

    found = False

    for source in sorted(graph.graph):
        dependencies = graph.dependencies_of(source)

        if not dependencies:
            continue

        found = True
        print(f"\n{source}")

        for dependency in sorted(dependencies):
            print(f"  -> {dependency}")

    if not found:
        print("No internal dependencies found.")


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


def main():
    parser = PythonDependencyParser()
    graph = parser.parse_repository(".")

    print("\nCODEPULSE REPOSITORY ANALYSIS")
    print("=" * 60)

    print_dependencies(graph)

    print("\n" + "=" * 60)
    print(
        f"Circular dependency detected: "
        f"{graph.has_cycle()}"
    )

    run_impact_analysis(graph)


if __name__ == "__main__":
    main()