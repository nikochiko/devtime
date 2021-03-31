Number.prototype.comma_formatter = function() {
    return this.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

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

            let ctx = document.getElementById("daywiseChart").getContext("2d");

            let dataPoints = [];

            if (this.data) {
                for (const [key, value] of Object.entries(this.data)) {
                    if (this.selectedLanguage) {
                        dataPoints.push(value.languages[this.selectedLanguage]);
                    } else {
                        dataPoints.push(value.total);
                    }
                }
            }

            let chart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: Object.keys(this.data),
                    datasets: [
                        {
                            label: "Time (in minutes)",
                            backgroundColor: "rgba(102, 126, 234, 0.25)",
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
        }
    }
};


let todaysStats = function(authToken, chartType="pie"){
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

            let ctx = document.getElementById("todaysStats").getContext("2d");

            let chart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: Object.keys(this.data.languages),
                    datasets: [
                        {
                            label: "Time (in minutes)",
                            backgroundColor: "rgba(102, 100, 234, 0.25)",
                            borderColor: "rgba(102, 126, 200, 1)",
                            pointBackgroundColor: "rgba(102, 200, 234, 1)",
                            data: Object.values(this.data.languages),
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
        }
    }
};

let prettifyMinutes = function(minutes) {
    let hours = Math.floor(minutes / 60);
    mins = minutes % 60;

    return hours > 0 ? `${hours}h ${mins}m` : `${mins} minutes`;
};
