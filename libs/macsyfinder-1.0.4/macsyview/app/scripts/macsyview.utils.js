// ┌──────────────────────────────────────────────────────────────────────┐ \\
// │ MacSyView - Visualization of MacSyFinder results.                    │ \\
// ├──────────────────────────────────────────────────────────────────────┤ \\
// │ Authors: Hervé Ménager, Bertrand Néron.                              │ \\
// │ Copyright © 2014 Institut Pasteur, Paris.                            │ \\
// │ See the COPYRIGHT file for details.                                  │ \\
// ├──────────────────────────────────────────────────────────────────────┤ \\
// │ MacSyView is distributed under the terms of the                      │ \\
// │ GNU General Public License (GPLv3). See the COPYING file for details.│ \\
// └──────────────────────────────────────────────────────────────────────┘ \\

/*
 * macsyview.utils
 * Ordered view for MacSyView
 */

/* jslint         browser : true, continue : true,
  devel  : true, indent  : 2,    maxerr   : 50,
  newcap : true, nomen   : true, plusplus : true,
  regexp : true, sloppy  : true, vars     : false,
  white  : true
 */

/*global $, macsyview */

macsyview.utils = (function () {
	'use strict';


	/*********************
	 *  Color Picker
	 *********************/
	var ColorPicker = function ColorPicker(){
		this.colorMap = [
		                 "Aqua", 
		                 "Bisque", "Blue", "BlueViolet", "Brown", "BurlyWood", 
		                 "CadetBlue", "Chartreuse", "Chocolate", "Coral", "CornflowerBlue", "Crimson", 
		                 "DarkCyan", "DarkGoldenRod", "DarkGreen", "DarkKhaki", "DarkMagenta", "DarkOliveGreen", 
		                 "DarkOrange", "DarkGoldenRod", "DarkKhaki", "DarkSalmon", "DarkSeaGreen", "DarkSlateBlue", "DarkSlateGray", "DeepPink", "DodgerBlue", 
		                 "FireBrick", 
		                 "Gold", "GreenYellow", 
		                 "HotPink",
		                 "IndianRed", "Indigo", 
		                 "Khaki",
		                 "LightCoral", "LightGreen", "LightPink", "LightSeaGreen", "LightSlateGray", 
		                 "MediumOrchid", "MediumSeaGreen", "MediumSlateBlue", "Moccasin", 
		                 "Olive", "OliveDrab", "Orange", "OrangeRed", 
		                 "PaleVioletRed", "Peru", "Plum", "Purple", 
		                 "Red", "RosyBrown", 
		                 "SaddleBrown", "Salmon", "SandyBrown", "SteelBlue",
		                 "Teal", "Tomato", 
		                 "Yellow", "YellowGreen" 
		                 ];

		this.defaultColor = "Gainsboro";
		this.pick = function(gene){
			var color = this.defaultColor;
			if(gene.match){
				var key = 0;
				for( var i = 0; i < gene.match.length; i++){
					key += (gene.match.charCodeAt(i) * (i + 1));
				};
				key %= this.colorMap.length;
				color = this.colorMap[key];
			}
			return color;
		}
	};

	ColorPicker.prototype.setMap = function (colorMap, defaultColor, pick){
		this.colorMap = colorMap;
		this.defaultColor = defaultColor;
		this.pick = pick;
	};
	return {
		colorPicker: new ColorPicker()
	};
}());
