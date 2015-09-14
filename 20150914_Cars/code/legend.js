"usestrict";
function buildYearLegend(svg, data, colScale){
    var yearList = buildYearList(data,"year")

    var originList = buildOriginList(data)

    // var buttonContainer = svg.append("g")
    //     .attr("class", "titleButton legend")
    //     .attr("transform", "translate(" + 125 + "," + 30 + ")")  
    //   .append("rect")
    //     .attr("class", "titleButton")
    //     .attr("width", 200)
    //     .attr("height", 30)
    //     .attr("x",-100)
    //     .attr("y", -15)
    //     .attr("rx", 5)
    //     .attr("ry", 5);
    // svg.select(".titleButton")
    //   .append("text")
    //     .attr("text-anchor", "middle")
    //     .text("Legend");
    var weightContainer = svg.append("g")
        .attr("class", "itemContainer legend")
        .attr("transform", "translate(" + 125 + "," + 5 + ")")

    var weightTitle = weightContainer
        .append("g")
        .attr("class", "title legend")
        .attr("transform", "translate(0,20)")
        .style("opacity", 1);

    weightTitle.append("text")
        .attr("x", -40)
        .attr("y", 30/2)
        .attr("transform", "translate(-50,0)")
        .text("symbol size -> car weight")

        //////////

    var originContainer = svg.append("g")
        .attr("class", "itemContainer legend")
        .attr("transform", "translate(" + 125 + "," + 55 + ")")

    var originTitle = originContainer
        .append("g")
        .attr("class", "title legend")
        .attr("transform", "translate(0,20)")
        .style("opacity", 1);

    originTitle.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(-50,0)")
        .text("origin")

    originTitle.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(50,0)")
        .text("#models")
    
    var origin = originContainer.selectAll(".origin")
                .data(originList)

    origin.enter()
        .append("g")
        .attr("class", "legend origin")
        .attr("transform", function(d,i){ return "translate(0," + (i + 2) * 20 + ")"})
        .style("opacity", 1);

    origin.append("path")
        .attr("d", function(p) { return genGlyph(p, 8)()})
        .style("fill", "#000")
        .attr("transform", "translate(-80,10)")
        
    origin.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(-50,0)")
        .text(function(d){return d["origin"];})

    origin.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(60,0)")
        .text(function(d){return d["nCars"];})

        ///////

    var yearContainer = svg.append("g")
        .attr("class", "itemContainer legend")
        .attr("transform", "translate(" + 125 + "," + 150 + ")")

    var yearTitle = yearContainer
        .append("g")
        .attr("class", "title legend")
        .attr("transform", "translate(0,20)")
        .style("opacity", 1);

    yearTitle.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(-50,0)")
        .text("year")

    yearTitle.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(50,0)")
        .text("#models")
    
    var year = yearContainer.selectAll(".year")
                .data(yearList)

    year.enter()
        .append("g")
        .attr("class", "legend year")
        .attr("transform", function(d,i){ return "translate(0," + (i + 2) * 20 + ")"})
        .style("opacity", 1);

    year.append("circle")
        .attr("r", 5)
        .attr("transform", "translate(-80,10)")
        .style("fill", function(d) {return "hsl(" +  colScale(yearList.indexOf(d) + 69)  + ",100%,50%)" })
       
    
    year.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(-50,0)")
        .text(function(d){return "19" + d["year"];})

    year.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(60,0)")
        .text(function(d){return d["nCars"];})

}



function buildBrandLegend(svg, data, colScale){
    var brandList = buildBrandList(data)

    var countryList = ["US","Europe","Japan"]

    var buttonContainer = svg.append("g")
        .attr("class", "titleButton legend")
        .attr("transform", "translate(" + 125 + "," + 30 + ")")  
      .append("rect")
        .attr("class", "titleButton")
        .attr("width", 200)
        .attr("height", 30)
        .attr("x",-100)
        .attr("y", -15)
        .attr("rx", 5)
        .attr("ry", 5);
    svg.select(".titleButton")
      .append("text")
        .attr("text-anchor", "middle")
        .text("Legend");

    var itemContainer = svg.append("g")
        .attr("class", "itemContainer legend")
        .attr("transform", "translate(" + 125 + "," + 30 + ")")
    var item = itemContainer.selectAll(".item")
                .data(brandList)

    item.enter()
        .append("g")
        .attr("class", "legendBrand")
        .attr("transform", function(d,i){ return "translate(0," + (i + 1) * 20 + ")"})
        .style("opacity", 1);

    item.append("circle")
        .attr("r", 5)
        .attr("transform", "translate(-80,10)")
        .style("fill", function(d) {return "hsl(" +  colScale(itemList.indexOf(d))  + ",100%,50%)" })
    
    item.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(-50,0)")
        .text(function(d){return d["item"];})

    item.append("text")
        .attr("x", 0)
        .attr("y", 30/2)
        .attr("transform", "translate(60,0)")
        .text(function(d){return d["nCars"];})
}