function render() {
    const file = document.getElementById("file").value;

    const priceColumnSelect = document.getElementById("price-column");
    const priceColumn = priceColumnSelect.options[priceColumnSelect.selectedIndex].value;

    const includeConsumption = document.getElementById("include-consumption").checked;

    const dates = [];
    const priceSeries = {};
    const consumptionSeries = {}

    d3.csv(file, function (err, rows) {
        const allKeys = Object.keys(rows[0]);

        const matchingPriceKeys = allKeys.filter((key) => key.toLowerCase().includes(`${priceColumn} price`.toLowerCase()));
        matchingPriceKeys.forEach((key) => priceSeries[key] = []);

        const matchingConsumptionKeys = allKeys.filter((key) => key.toLowerCase().includes("consumption"));
        matchingConsumptionKeys.forEach((key) => consumptionSeries[key] = []);

        rows.forEach((row) => {
            dates.push(row["Start"]);
            matchingPriceKeys.forEach((key) => priceSeries[key].push(row[key]));
            matchingConsumptionKeys.forEach((key) => consumptionSeries[key].push(row[key]));
        });

        const priceData = matchingPriceKeys.map((key) => {
            return {
                type: "scatter",
                mode: "lines",
                name: key.split(" --- ")[0],
                x: dates,
                y: priceSeries[key],
            };
        });

        const consumptionData = matchingConsumptionKeys.map((key) => {
            return {
                type: "scatter",
                mode: "lines",
                name: key,
                x: dates,
                y: consumptionSeries[key],
                yaxis: "y2",
            };
        });

        const layout = {
            title: {text: `${priceColumn} price (GBP)`},
            xaxis: {
                rangeslider: {range: [dates[0], dates[-1]]},
                type: "date",
            },
            yaxis: {
                type: "linear",
            }
        };

        if (includeConsumption) {
            layout["title"]["text"] = `Top: ${priceColumn} price (GBP) --- Bottom: Electricity consumption (kwh)`
            layout["yaxis"]["domain"] = [0.5, 1];
            layout["yaxis2"] = {
                type: "linear",
                domain: [0, 0.5]
            };
            Plotly.newPlot("graph-container", priceData.concat(consumptionData), layout);
        } else {
            Plotly.newPlot("graph-container", priceData, layout);
        }
    });
}