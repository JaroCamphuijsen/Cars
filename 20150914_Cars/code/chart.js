"usestrict";

var menuTimeout;

function buildChart(data, dimDict, svg){
/*
The Multi point View and all of its parts is initiated 
*/

    // Initiate the axis containers first, so they will be at the lowest 
    // level in the svg, and transform them into place.
    var xContainer = svg.append("g")
        .attr("class", "x axisContainer")
        .attr("transform", "translate(0," + (chartHeight - chartPadding) + ")");

    var yContainer = svg.append("g")
        .attr("class", "y axisContainer")
        .attr("transform", "translate(" + chartPadding + ",0)");

    // appending containers for the actual axis scales
    xContainer.append("g")
        .attr("class", "axis x");
    yContainer.append("g")
        .attr("class", "axis y");

    // appending the axis titles and axis scales the axis containers
    xContainer.append("g")
        .attr("class", "axisTitle x")
        .attr("transform", "translate(" + (((chartWidth - chartPadding)/2) + 
                chartPadding) + "," + 40 + ")")  
      .append("rect")
        .attr("class", "titleButton")
        .attr("width", 250)
        .attr("height", 30)
        .attr("x",-125)
        .attr("y", -15)
        .attr("rx", 5)
        .attr("ry", 5);
    xContainer.select(".axisTitle")
      .append("text")
        .attr("text-anchor", "middle");
 
    yContainer.append("g")
        .attr("class", "axisTitle y")
        .attr("transform", "translate(" + -70 + ", " + 
                ((chartHeight - chartPadding)/2) + ") rotate(270)")
      .append("rect")
        .attr("class", "titleButton")
        .attr("width", 250)
        .attr("height", 30)
        .attr("x",-125)
        .attr("y", -15)
        .attr("rx", 5)
        .attr("ry", 5);
    yContainer.select(".axisTitle")
      .append("text")
        .attr("text-anchor", "middle");

    // Initiate the plotcontainer next, so dots are drawn on top of the axes
    svg.append("g")
        .attr("id", "plotContainer");
        
    // Initiate the dropdown menu for choosing the plotted dimension last
    // so it will be on top of the scatterplot and axes
    svg.append("g")
        .attr("class","plotMenu")
        .attr("transform", "translate(" + (((chartWidth - chartPadding)/2) + 
                chartPadding) + ", " + ((chartHeight - chartPadding)/2) + ")");
}

function updateScatter(data, dimDict, svg, xAttr, yAttr, sizeAttr, colAttr, valAttr){
    /*
    Updates the old scatterplot to scatterplot with new dimensions xAttr and
    yAttr in the multipointview. Using sexy transitions.
    */
    // Filter the data for the chosen dimensions so all datapoints without a 
    // value for x or y will not be drawn.
   
    var brandList = buildBrandList(data);
    var selData = filterData(data, xAttr, yAttr);

    var dataXRange = d3.extent(selData, function(p){return Number(p[xAttr]);});
    var dataYRange = d3.extent(selData, function(p){return Number(p[yAttr]);});
    var dataSizeRange = d3.extent(selData, function(p){return Number(p[sizeAttr]);});
    var dataValRange = d3.extent(selData, function(p){return Number(p[colAttr]);});
    var dataColRange = d3.extent(selData, function(p){return Number(p[colAttr]);});
    var chartXScale = d3.scale
        .linear()
        .range([chartPadding, chartWidth - 10])
        .domain([dataXRange[0] - .05*dataXRange[1], 1.05*dataXRange[1]]);
    var chartYScale = d3.scale
        .linear()
        .range([chartHeight - chartPadding, 20])
        .domain([dataYRange[0] - .05*dataYRange[1], 1.05*dataYRange[1]]);
    var chartSizeScale = d3.scale
        .linear()
        .range([4, 12])
        .domain(dataSizeRange);
    var chartValScale = d3.scale
        .linear()
        .range([20,50])
        .domain(dataValRange);
    var chartColScale = d3.scale
        .linear()
        .range([0,100])
        .domain(dataColRange);

    // A selection of the available dimensions in the data is selected, 
    // because many of the original dimensions are to specific or not plottable
    var chartDimensions = ["MPG","cylinders","horsepower","weight","year"];
    var originColorMap = {"Europe": "rgb(0,0,255)", "US": "rgb(255,255,0)", "Japan": "rgb(255,0,0)"}
    var brandColorMap = {}

    var xAxis = d3.svg.axis().scale(chartXScale).orient("bottom");
    var yAxis = d3.svg.axis().scale(chartYScale).orient("left");
    var plotContainer = svg.select("#plotContainer");

    // transitions for the axes to the new scales
    svg.select(".x.axisContainer")
      .select(".x.axis")
        .transition()
        .duration(1500)
        .call(xAxis);

    svg.select(".y.axisContainer")
      .select("g.y.axis")
        .transition()
        .duration(1500)
        .call(yAxis);

    // transition for the axis titles to the new titles
    svg.select("g.x.axisTitle")
        .on("mouseover", function(p){
            svg.select("g.x.axisTitle")
                .select("rect")
                .classed("highlight", true);
            })
        .on("mouseout", function(p){
            svg.select("g.x.axisTitle")
                .select("rect")
                .classed("highlight", false);
            })
        .on("click", function(p){
            showPlotMenu(data, chartDimensions, dimDict, svg, xAttr, yAttr, sizeAttr, colAttr, "x");
            })
        .transition()
        .duration(1500)
        .select("text")
        .attr("dy", ".35em")
        .text(findDimAttr(dimDict, xAttr, "label") + "(" + findDimAttr(dimDict, xAttr, "unit") + ")");

    svg.select("g.y.axisTitle")        
        .on("mouseover", function(p){
                svg.select("g.y.axisTitle")
                    .select("rect")
                    .classed("highlight", true);
            })
        .on("mouseout", function(p){
            svg.select("g.y.axisTitle")
                .select("rect")
                .classed("highlight", false);
            })
        .on("click", function(p){
            showPlotMenu(data, chartDimensions, dimDict, svg, xAttr, yAttr, sizeAttr, colAttr, "y");
            })
        .transition()
        .duration(1500)
        .select("text")
        .attr("dy", ".35em")
        .text(findDimAttr(dimDict, yAttr, "label") + "(" + findDimAttr(dimDict, yAttr, "unit") + ")");
     
    // data-join with model as keyfunction
    var points = plotContainer.selectAll(".dot")
        .data(selData, function(p) {return p.model});

    // update old data
    points.transition()
        .duration(1500)
        .attr("transform", function(p) {return "translate(" + (chartXScale(p[xAttr])) + "," + chartYScale(p[yAttr]) + ")"})
        .attr();

    // // update old data
    // points.transition()
    //     .duration(1500)
    //     .attr("cx", function(p) {return (chartXScale(p[xAttr]))})
    //     .attr("cy", function(p) {return (chartYScale(p[yAttr]))})
    //     .attr();
    
    // select and update the selected point
    plotContainer.selectAll(".selDot")
        .transition()
        .duration(1500)
        .attr("transform", function(p) {
                return "translate(" + chartXScale(p[xAttr]) + "," + chartYScale(p[yAttr]) + ")"}
                );
        
    // // select and update the selected point
    // plotContainer.selectAll(".selDot")
    //     .transition()
    //     .duration(1500)
    //     .attr("cx", function(p) {
    //         if (Number(p[xAttr]) != 0){
    //         return chartXScale(p[xAttr]);}
    //         else{ return (chartPadding - 5);}
    //     })
    //     .attr("cy", function(p) {
    //         if (Number(p[yAttr]) != 0){
    //         return chartYScale(p[yAttr]);}
    //         else{return ((chartHeight - chartPadding) + 5);}});

    // enter new data
    

    points.enter()
        .insert("path", ".sameVal .selDot")
        .attr("d", function(p) { return genGlyph(p, chartSizeScale(p[sizeAttr]))()})
        .classed("dot", true)
        .style("fill-opacity", 0)
        .attr("transform", function(p) {return "translate(" + (chartXScale(p[xAttr])) + "," + chartYScale(p[yAttr]) + ")"})
        .style("fill",function(p) {return "hsl(" +  chartColScale(p["year"])  + ",100%,50%)" })
        .transition()
        .duration(1500)
        .style("fill-opacity", 1)
                
// the style statement for the use of a brandcolormap
        // .style("fill",function(p) {return "hsl(" +  chartColScale(findWithAttr(brandList, "brand", getBrand(p["model"])))  + ",100%,50%)" })

// using a origin colormap
    // points.enter()
    //     .insert("circle", ".sameVal, .selDot")
    //     .classed("dot", true)
    //     .style("fill-opacity", 0)
    //     .attr("cx", function(p) {return (chartXScale(p[xAttr]))})
    //     .attr("cy", function(p) {return (chartYScale(p[yAttr]))})
    //     .attr("r", function(p) { return (chartSizeScale(p[sizeAttr]))})
    //     .style("fill",function(p) { return (originColorMap[p["origin"]])} )
    //     .transition()
    //     .duration(1500)
    //     .style("fill-opacity", 1)



    // exit old data
    points.exit()
        .classed("exit", true)
        .transition()
        .duration(1500)
        .style("fill-opacity", 0)
        .remove();

    // highlighting datapoints when hovering and selecting one datapoint on 
    // clicking the selected datapoint is also sent to the Single point View 
    // through the "toSpv" function
    points.on("mouseover", function(p){
            d3.select(d3.event.target)
                .classed("highlight", true);
            })
        .on("mouseout", function(p){
            d3.select(d3.event.target)
                .classed("highlight", false);
            })
        .on("click", function(p){
            showInfo(p, infoDiv);
            drawSelDot(p, chartXScale(p[xAttr]), chartYScale(p[yAttr]), chartSvg);
            });

    buildYearLegend(legendSvg, data, chartColScale);
}

function drawSelDot(point, x, y, svg){
    var plotContainer = svg.select("#plotContainer");
    plotContainer.selectAll(".selDot")
        .transition()
        .duration(400)
        .attr("r", 0)
        .remove()

    var selPoint = plotContainer.selectAll(".selDot")
        .data([point], function(d) {return d.model})
        
    selPoint.enter()
        .append("circle")
        .attr("class", "selDot")
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", 0)
        .transition()
        .duration(400)
        .attr("r", 8);
}

function showPlotMenu(data, dimensions, dimDict, svg, xAttr, yAttr, sizeAttr, colAttr, axis) {
    /*
    Function to show the menu for changing the axis dimension.
    */
    var buttonWidth = 100;
    var buttonHeight = 30;
    
    // for each menu (y and x), the start and end positions are defined
    if (axis === "x"){
        var start = function(d,i){return "translate(-51,400)"}; 
        var end = function(d, i) { 
            return "translate(-51," + ( i ) * buttonHeight + ")"
            };
    }
    if (axis === "y"){
        var start = function(d, i) { 
            return "translate(-700," + (i - dimensions.length/2) * buttonHeight + ")"
            };
        
        var end = function(d, i) { 
            return "translate(-400," + (i - dimensions.length/2) * buttonHeight + ")"
            };
      
    }

    // button databinding
    var button = svg.select(".plotMenu")
        .selectAll(".plotMenuButton")
        .data(dimensions);

    // button enterselection, appended with starting position and a transition
    // to the end position of each button
    button.enter()
        .append("g")
        .attr("class", "plotMenuButton")
        .style("opacity", 0)
        .attr("transform", function(d,i){ return start(d,i)})
        .transition()
        .duration(800)
        .attr("transform", function(d,i){ return end(d,i)})
        .style("opacity", 1);
    
    // contents of each button
    button.append("rect")
        .attr("width", 100)
        .attr("height", 0)
        .attr("height", buttonHeight - 1)
    
    button.append("text")
        .attr("dx", ".35em")
        .attr("y", buttonHeight / 2)
        .attr("dy", ".35em")
        .text(function(d){return d;})

    // interactivity of the menubuttons with updateScatter call
    button.on("mouseover", function(p){
            d3.select(d3.event.target.parentNode)
                .classed("highlight", true); 
            // explainDim(p, explainDimDiv);
            })
        .on("mouseout", function(p){
            d3.select(d3.event.target.parentNode)
                .classed("highlight", false);
            })
        .on("click", function(p){
            if (axis === "x") {xAttr = p}
            if (axis === "y") {yAttr = p}
            updateScatter(data, dimDict, svg, xAttr, yAttr, sizeAttr, colAttr);

        });

// When the plotmenu is on screen, clicking anywhere in the svg will make the 
// menu disappear. A timeout is needed, otherwise clicking on the menubutton 
// will simultaneously open and close the menu, so no menu is shown at all.
    menuTimeout = setTimeout(function(d){svg.on("click", function(p){
                clearMenu(svg, start); 

                svg.on("click", function(){});
            });
        }, 5);

}

function clearMenu(svg, end){
    /*
    This funcion clears the menu in a smooth transition.
    */
    
    clearTimeout(menuTimeout);
    svg.select(".plotMenu")
        .selectAll(".plotMenuButton")
        .transition()
        .duration(800)
        .style("opacity", 0)
        .attr("transform", function(d,i){return end(d,i)})
        .remove()
}


