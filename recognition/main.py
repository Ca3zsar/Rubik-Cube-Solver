import color_analyzer

expected_file = "samples/expected.txt"

def main():
    expected_results = []
    with open(expected_file, "r") as f:
        for line in f:
            expected_results.append(
                list(map(int, line.strip().split(",")))
            )

    for i in range(len(expected_results)):
        actual_results = color_analyzer.apply_operations(
            show = False,
            crop = False,
            rotate = False,
            image_name = f"samples/sample_{i}.jpg",
            return_data = True
        )
        # print(f"{i} {actual_results}")
        # print(f"{i} {expected_results[i]}")
        
        if actual_results == expected_results[i]:
            print(f"Sample {i} is correct")
        else:
            print(f"Sample {i} is incorrect")
            print(f"Expected: {expected_results[i]}")
            print(f"Actual  : {actual_results}")
        print("------")


if __name__ == "__main__":
    main()