$(document).ready(function () {
    d3.json("./static/scripts/constants.json").then((data) => {
        data = data[0]

        for (const val in data.primary_stone) {
            const valDict = data.primary_stone[val];
            if (Object.keys(valDict).length !== 0) {
                for (const prop in valDict) {
                    $("#primary-" + val + "-" + prop + "-dropdown select").hide();
                    $("#primary-" + val + "-radio").change(function () {
                        if ($(this).is(":checked")) {
                            $("#primary-" + val + "-" + prop + "-dropdown select").show();
                        } else {
                            $("#primary-" + val + "-" + prop + "-dropdown select").hide();
                        }
                    })
                }
            }
        }

        for (const val in data.secondary_stones) {
            const valDict = data.secondary_stones[val];
            if (Object.keys(valDict).length !== 0) {
                for (const prop in valDict) {
                    const idVal = val.replaceAll(" ", "-")
                    $("#secondary-" + idVal + "-" + prop + "-dropdown select").hide();
                    $("#secondary-" + idVal + "-checkbox").change(function () {
                        $("#secondary-" + idVal + "-" + prop + "-dropdown select").hide();
                        if ($(this).is(":checked")) {
                            $("#secondary-" + idVal + "-" + prop + "-dropdown select").show();
                        } else {
                            $("#secondary-" + idVal + "-" + prop + "-dropdown select").hide();
                        }
                    })
                }
            }
        }
    });
})
