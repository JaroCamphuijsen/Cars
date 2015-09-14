"usestrict";
/*
Variable declaration. 
    chartDiv          => Multi Planet View div, the div for scatterplot or skymap
    legendDiv          => Single Planet View div, here we'll see the planet's orbit
    spInfoDiv       => Single Planet Info div, showing extra information about
                        the selected planet
    explainDimDiv   => explain dimensions div, with a short description of 
                        the selected dimension
*/
var body = d3.select("body"),
    chartDiv = body.select("#chartDiv"),
    legendDiv = body.select("#legendDiv"),
    infoDiv = body.select("#infoDiv"),
    explainDimDiv = body.select("#explainDimDiv"),
    chartWidth = 1000, chartHeight = 500,
    // legendWidth = 400, legendHeight = 400,
    chartSize = function() {return chartDiv.node().getBoundingClientRect();},
    legendSize = function() {return legendDiv.node().getBoundingClientRect();},
    spInfoSize = function() {return spInfoDiv.node().getBoundingClientRect();},
    explainDimSize = function() {return explainDimDiv.node().getBoundingClientRect();},
    chartPadding = 100,
    nCols = 3, rDot = 2.4; 



/*
Initiating the visualization svg's
*/

var chartSvg = chartDiv.append("svg")
    .attr("width", chartWidth + "px")
    .attr("height", chartHeight + "px")
    .attr("class", "chartSvg");

var legendSvg = legendDiv.append("svg")
    .attr("width", 250 + "px")
    .attr("height", 500 + "px")
    .attr("class", "legendSvg");


d3.csv("cars.csv", function(data){
    d3.csv("carsDim.csv", function(dimDict){
        buildChart(data, dimDict, chartSvg );
        updateScatter(data, dimDict, chartSvg, "MPG", "horsepower", "weight", "year");


    });
});

