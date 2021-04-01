Number.prototype.comma_formatter = function() {
    return this.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

let compareDatesInDDMMYY = function(a, b) {
    let [dayA, monthA, yearA] = a.split('-');
    let [dayB, monthB, yearB] = b.split('-');

    // -1 if a < b, 1 if a > b, and 0 if a == b
    if (yearA === yearB) {
        return monthA === monthB ? Number(dayA) - Number(dayB) : Number(monthA) - Number(monthB);
    } else {
        return Number(yearA) - Number(yearB);
    }
};

let capitalize = function(x) {
    return x.charAt(0).toUpperCase() + x.slice(1);
};

let chartData = function(authToken, chartType="line"){
    return {
        date: 'today',
        timelineOptions: [
            {
                label: 'Last 7 days',
                value:  '7days',
                start: new Date(Date.now() - (7 * 24 * 60 * 60 * 1000)),
                end: new Date(Date.now() + (24 * 60 * 60 * 1000))
            },
            {
                label: 'Last 30 days',
                value: '30days',
                start: new Date(Date.now() - (30 * 24 * 60 * 60 * 1000)),
                end: new Date(Date.now() + (24 * 60 * 60 * 1000))
            },
            {
                label: 'Last 6 Months',
                value: '6months',
                start: new Date(Date.now() - (180 * 24 * 60 * 60 * 1000)),
                end: new Date(Date.now() + (24 * 60 * 60 * 1000))
            },
            {
                label: 'This Year',
                value: 'year',
                start: new Date(Date.now() - (365 * 24 * 60 * 60 * 1000)),
                end: new Date(Date.now() + (24 * 60 * 60 * 1000))
            },
        ],
        languageOptions: [
            {
                label: 'Select Language',
                value: null,
            }
        ],
        showDropdown: false,
        selectedOption: 0,
        selectedLangauge: null,
        selectOption: function(index){
            this.selectedOption = index;
            this.fetch();
            this.renderChart();
        },
        selectLanguage: function(index){
            this.selectedLanguage = index;
            this.renderChart();
        },
        data: null,
        fetch: function(){
            let startIso = this.timelineOptions[this.selectedOption].start.toISOString();
            let endIso = this.timelineOptions[this.selectedOption].end.toISOString(); 
            let url = `/api/daywise_stats?start=${startIso}&end=${endIso}`;
            fetch(url, { method: "GET", headers: { Authorization: `token ${authToken}` } })
                .then(res => res.json())
                .then(res => {
                    this.data = res;
                    this.renderChart();
                    Object.keys(res.languages || {}).forEach(lang => {
                        this.languageOptions.push({
                            // capitalize in label
                            label: lang.charAt(0).toUpperCase() + lang.slice(1),
                            value: lang,
                        })
                    });
                })
        },
        renderChart: function(){
            let c = false;

            Chart.helpers.each(Chart.instances, function(instance) {
                if (instance.chart.canvas.id == 'daywiseStats') {
                    c = instance;
                }
            });

            if(c) {
                c.destroy();
            }

            let canvas = document.getElementById("daywiseChart")
            let ctx = canvas.getContext("2d");

            let sortedDates = Object.keys(this.data);
            sortedDates.sort(compareDatesInDDMMYY);
            
            let dataPoints = [];
            for (const date of sortedDates) {
                if (this.selectedLanguage) {
                    dataPoints.push(this.data[date].languages[this.selectedLanguage]);
                } else {
                    dataPoints.push(this.data[date].total);
                }
            }

            let chart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: sortedDates,
                    datasets: [
                        {
                            label: "Time (in minutes)",
                            backgroundColor: "rgba(29, 78, 216, 0.33)",
                            borderColor: "rgba(102, 126, 234, 1)",
                            pointBackgroundColor: "rgba(102, 126, 234, 1)",
                            data: dataPoints,
                        },
                    ],
                },
                layout: {
                    padding: {
                        right: 10
                    }
                },
                options: {
                    scales: {
                        yAxes: [{
                            gridLines: {
                                display: false
                            },
                        }]
                    }
                }
            });

            canvas.style.width ='100%';
            canvas.style.height='100%';
            canvas.width  = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
        }
    }
};

function colorChart(ctx, chart) {
    let palette = ["cool", "warm", "neon"][Math.floor(Math.random() * 3)];

    /*Gradients
      The keys are percentage and the values are the color in a rgba format.
      You can have as many "color stops" (%) as you like.
      0% and 100% is not optional.*/
    var gradient;
    switch (palette) {
        case 'cool':
            gradient = {
                0: [255, 255, 255, 1],
                20: [220, 237, 200, 1],
                45: [66, 179, 213, 1],
                65: [26, 39, 62, 1],
                100: [0, 0, 0, 1]
            };
            break;
        case 'warm':
            gradient = {
                0: [255, 255, 255, 1],
                20: [254, 235, 101, 1],
                45: [228, 82, 27, 1],
                65: [77, 52, 47, 1],
                100: [0, 0, 0, 1]
            };
            break;
        case 'neon':
            gradient = {
                0: [255, 255, 255, 1],
                20: [255, 236, 179, 1],
                45: [232, 82, 133, 1],
                65: [106, 27, 154, 1],
                100: [0, 0, 0, 1]
            };
            break;
    }

    //Get a sorted array of the gradient keys
    var gradientKeys = Object.keys(gradient);
    gradientKeys.sort(function(a, b) {
        return +a - +b;
    });

    //Find datasets and length
    var chartType = chart.config.type;
    switch (chartType) {
        case "pie":
        case "doughnut":
            var datasets = chart.config.data.datasets[0];
            var setsCount = datasets.data.length;
            break;
        case "bar":
        case "line":
            var datasets = chart.config.data.datasets;
            var setsCount = datasets.length;
            break;
    }

    //Calculate colors
    var chartColors = [];
    for (i = 0; i < setsCount; i++) {
        var gradientIndex = (i + 1) * (100 / (setsCount + 1)); //Find where to get a color from the gradient
        for (j = 0; j < gradientKeys.length; j++) {
            var gradientKey = gradientKeys[j];
            if (gradientIndex === +gradientKey) { //Exact match with a gradient key - just get that color
                chartColors[i] = 'rgba(' + gradient[gradientKey].toString() + ')';
                break;
            } else if (gradientIndex < +gradientKey) { //It's somewhere between this gradient key and the previous
                var prevKey = gradientKeys[j - 1];
                var gradientPartIndex = (gradientIndex - prevKey) / (gradientKey - prevKey); //Calculate where
                var color = [];
                for (k = 0; k < 4; k++) { //Loop through Red, Green, Blue and Alpha and calculate the correct color and opacity
                    color[k] = gradient[prevKey][k] - ((gradient[prevKey][k] - gradient[gradientKey][k]) * gradientPartIndex);
                    if (k < 3) color[k] = Math.round(color[k]);
                }
                chartColors[i] = 'rgba(' + color.toString() + ')';
                break;
            }
        }
    }

    //Copy colors to the chart
    for (i = 0; i < setsCount; i++) {
        switch (chartType) {
            case "pie":
            case "doughnut":
                if (!datasets.backgroundColor) datasets.backgroundColor = [];
                datasets.backgroundColor[i] = chartColors[i];
                if (!datasets.borderColor) datasets.borderColor = [];
                datasets.borderColor[i] = "rgba(255,255,255,1)";
                break;
            case "bar":
                datasets[i].backgroundColor = chartColors[i];
                datasets[i].borderColor = "rgba(255,255,255,0)";
                break;
            case "line":
                datasets[i].borderColor = chartColors[i];
                datasets[i].backgroundColor = "rgba(255,255,255,0)";
                break;
        }
    }

    //Update the chart to show the new colors
    chart.update();
}

let todaysStats = function(authToken, chartType="doughnut"){
    return {
        data: null,
        fetch: function(){
            let startIso = new Date(Date.now() - 24 * 60 * 60 * 1000);
            let endIso = new Date(Date.now() + 24 * 60 * 60 * 1000);
            let url = `/api/activity?start=${startIso.toISOString()}&end=${endIso.toISOString()}`;
            fetch(url, { method: "GET", headers: { Authorization: `token ${authToken}` } })
                .then(res => res.json())
                .then(res => {
                    this.data = res;
                    this.renderChart();
                })
        },
        renderChart: function(){
            let c = false;

            Chart.helpers.each(Chart.instances, function(instance) {
                if (instance.chart.canvas.id == 'todaysStats') {
                    c = instance;
                }
            });

            if(c) {
                c.destroy();
            }

            let canvas = document.getElementById("todaysStats");
            let ctx = canvas.getContext("2d");

            let chart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: Object.keys(this.data.languages).map(capitalize),
                    datasets: [
                        {
                            label: "Time (in minutes)",
                            data: Object.values(this.data.languages),
                        },
                    ],
                },
                layout: {
                    padding: {
                        right: 10
                    }
                }
            });

            colorChart(ctx, chart);

            c = false;

            Chart.helpers.each(Chart.instances, function(instance) {
                if (instance.chart.canvas.id == 'todaysEditorStats') {
                    c = instance;
                }
            });

            if(c) {
                c.destroy();
            }

            canvas = document.getElementById("todaysEditorStats");
            ctx = canvas.getContext("2d");

            chart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: Object.keys(this.data.editors).map(capitalize),
                    datasets: [
                        {
                            label: "Time (in minutes)",
                            data: Object.values(this.data.editors),
                        },
                    ],
                },
                layout: {
                    padding: {
                        right: 10
                    }
                }
            });

            colorChart(ctx, chart);
        }
    }
};

let customDayChart = function(authToken, date) {
    date = new Date(date);
    let chartType = "doughnut";

    return {
        data: null,
        fetch: function(){
            let startIso = new Date(date - 24 * 60 * 60 * 1000);
            let endIso = new Date(date + 24 * 60 * 60 * 1000);
            let url = `/api/activity?start=${startIso.toISOString()}&end=${endIso.toISOString()}`;
            fetch(url, { method: "GET", headers: { Authorization: `token ${authToken}` } })
                .then(res => res.json())
                .then(res => {
                    this.data = res;
                    this.renderChart();
                })
        },
        renderChart: function(){
            let c = false;

            Chart.helpers.each(Chart.instances, function(instance) {
                if (instance.chart.canvas.id == "customDateChart") {
                    c = instance;
                }
            });

            if(c) {
                c.destroy();
            }

            let canvas = document.getElementById("customDateChart");
            let ctx = canvas.getContext("2d");

            let chart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: Object.keys(this.data.languages).map(capitalize),
                    datasets: [
                        {
                            label: "Time (in minutes)",
                            data: Object.values(this.data.languages),
                        },
                    ],
                },
                layout: {
                    padding: {
                        right: 10
                    }
                }
            });

            colorChart(ctx, chart);

            // c = false;

            // Chart.helpers.each(Chart.instances, function(instance) {
            //     if (instance.chart.canvas.id == 'customDateChartEditor') {
            //         c = instance;
            //     }
            // });

            // if(c) {
            //     c.destroy();
            // }

            // canvas = document.getElementById("todaysEditorStats");
            // ctx = canvas.getContext("2d");

            // chart = new Chart(ctx, {
            //     type: chartType,
            //     data: {
            //         labels: Object.keys(this.data.editors).map(capitalize),
            //         datasets: [
            //             {
            //                 label: "Time (in minutes)",
            //                 data: Object.values(this.data.editors),
            //             },
            //         ],
            //     },
            //     layout: {
            //         padding: {
            //             right: 10
            //         }
            //     }
            // });

            // colorChart(ctx, chart);
        }
    }
};

let prettifyMinutes = function(minutes) {
    let hours = Math.floor(minutes / 60);
    mins = minutes % 60;

    return hours > 0 ? `${hours}h ${mins}m` : `${mins} minutes`;
};
