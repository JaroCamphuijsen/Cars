"usestrict";

function filterData(data, xAttr, yAttr) {
    /*
    Function to filter the data given two dimensions. Any data without one of
    the attributes is not returned.
    */
    var d, newData = [];
        for (d = 0; d < data.length; d++) {
            if (Number(data[d][xAttr]) != 0 && Number(data[d][yAttr]) != 0) {
                newData.push(data[d]);
            }
        }
    return newData;
}

function addClass(points, dim, val, newClass, assign){
    /*
    Function to add or remove a class to specific datapoints.
    */
    assign = typeof assign !== "undefined" ?  assign : true;

    points.classed(newClass, function(d){
        if (d[dim] == val){return assign;}
        else{return false}});
}

function findDimAttr(dimDict, dimension, attr){
    // find the corresponding entry in the dimDict of a given dimension
    // and select the given attribute
    for (d in dimDict){
        if (dimension === dimDict[d]["name"]){
            return dimDict[d][attr];
        }
    }
}
function genGlyph(point, size){
	switch(point["origin"]){
		    case "US":
		    	return d3.svg.symbol()
            		.type("triangle-up")
            		.size(Math.pow(0.9*size,2));
                // break;
                
        case "Europe":
        	return calculateStarPoints(0,0,5,0.8*size, 0.4*size)
            // break;
        
        case "Japan":                
            return d3.svg.symbol()
        		.type("circle")
        		.size(Math.pow(size,2));
            // break;

        }
    }
function showInfo(point, div){
  div.html(genHTML(point))
}
function genHTML(point){
  return ("The <b>" + point["model"] + "</b> was built in the year <b>19" + point["year"] + 
  "</b> in  <b>" + point["origin"] + "</b>. With its <b>" + point["horsepower"] + "</b> horsepower, <b>" + 
  point["cylinders"] + "</b> cylinder engine and weight of <b>" + point["weight"] + "</b> lbs, it runs an avarage <b>" + point["MPG"] + "</b> miles per gallon. ")
}

//
function calculateStarPoints(centerX, centerY, arms, outerRadius, innerRadius)
{
   var results = "";

   var angle = Math.PI / arms;

   for (var i = 0; i < 2 * arms; i++)
   {
      // Use outer or inner radius depending on what iteration we are in.
      var r = (i & 1) == 0 ? outerRadius : innerRadius;
      
      var currX = centerX + Math.cos(i * angle) * r;
      var currY = centerY + Math.sin(i * angle) * r;

      // Our first time we simply append the coordinates, subsequet times
      // we append a ", " to distinguish each coordinate pair.
      if (i == 0)
      {
         results = "M" + currX + "," + currY;
      }
      else
      {
         results += "L" + currX + "," + currY;
      }
   }

   return function(){return results};
}

function getBrand(model){
	return model.split(" ")[0]
}

function findWithAttr(array, attr, value) {
    for(var i = 0; i < array.length; i += 1) {
        if(array[i][attr] === value) {
            return i;
        }
    }
}

function buildYearList(data) {
	var yearList = [];
	    var dataRange = d3.extent(data, function(p){return Number(p["year"]);});
	    
	    for (i = dataRange[0]; i <= dataRange[1]; i++){
        yearList.push({"year": String(i), "nCars": 0 })
      }

    	for (d = 0; d < data.length; d++){
	           	// console.log(yearList, year, data[d]["year"])
	            yearList[findWithAttr(yearList, "year", data[d]["year"])].nCars++
	                
	    }
	    
	    
	 return yearList
    }

function buildOriginList(data) {
  var origins = ["US", "Europe", "Japan"];
  var originList = [];    
      for (i = 0; i < origins.length; i++){
        originList.push({"origin": origins[i], "nCars": 0 })
      }

      for (d = 0; d < data.length; d++){
              // console.log(attrList, attr, data[d]["year"])
              originList[findWithAttr(originList, "origin", data[d]["origin"])].nCars++
                  
      }
      
      
   return originList
    }

function buildBrandList(data) {
	var brandUList = [], brandList = [], countries = ["US","Europe","Japan"];
	    var brand = ""
	    for (i = 0; i < data.length; i++){
	        brand = getBrand(data[i]["model"]); 
	        index = findWithAttr(brandUList, "brand", brand);
	        try {
	            brandUList[index].nCars++
	        } 
	        catch(err){
	        	brandUList.push({"brand": brand, "nCars": 1, "origin": data[i]["origin"] })
	        }
	    }
	    for (c = 0; c < countries.length; c++){
	    	for (i = 0; i < brandUList.length; i++){
	    		if (brandUList[i]["origin"] == countries[c]){
	    			brandList.push(brandUList[i])
	    		}
	    	}
	    }
	return brandList
    }

