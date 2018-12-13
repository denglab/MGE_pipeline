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
 * macsyview.data
 * data module for macsyview
 */

/* jslint   browser : true, continue : true,
  devel  : true, indent  : 4,    maxerr   : 50,
  newcap : true, nomen   : true, plusplus : true,
  regexp : true, sloppy  : true, vars     : false,
  white  : true
 */

/*global $, macsyview, FileReader, console */

macsyview.data = (function () {
    'use strict';

    var loadFile,
        load,
        reset,
        presence,
        isOrdered = false,
        list = [];

    reset = function () {
        list = [];
    };

    presence = ["mandatory", "accessory", "forbidden"];
    
    loadFile = function (textFileHandle, loadedCallback) {
        var result = "",
            chunkSize = 20000,
            fileSize = textFileHandle.size;

        function readBlob(file, offset) {
            //console.log("reading file at offset ", offset);
            var stop = offset + chunkSize - 1,
                reader,
                blob;
            if (stop > (fileSize - 1)) {
                stop = fileSize - 1;
            }
            reader = new FileReader();
            // If we use onloadend, we need to check the readyState.
            reader.onloadend = function (evt) {
                if (evt.target.readyState === FileReader.DONE) { // DONE == 2
                    result += evt.target.result;
                    if (stop < fileSize - 1) {
                        offset = offset + chunkSize;
                        evt = null;
                        readBlob(file, offset);
                    } else {
                        loadedCallback(result);
                    }
                }
            };
            blob = file.slice(offset, stop + 1);
            reader.readAsBinaryString(blob);
        }
        readBlob(textFileHandle, 0);
    };

    load = function (jsonFileHandle, callback) {
        loadFile(jsonFileHandle, function (jsonText) {
            var i, j;
            console.log('parsing json begins...');
            list = JSON.parse(jsonText);
            list.macsyviewId = Date.now();
            console.log('parsing json finished!');
            var utils = macsyview.utils;
            var colorPicker = utils.colorPicker;
            if (list[0] !== undefined && list[0].occurrence_number !== undefined) {
                isOrdered = true;
            }else{
                isOrdered = false;
            }
            for (i = 0; i < list.length; i++) {
                 //list[i].id = i; //TODO remove as soon as Bertrand provides the ID
                for (j = 0; j < list[i].genes.length; j++) {
                    var g = list[i].genes[j];
                    var c = colorPicker.pick(g);
                    g.color =  c;
                    if (g.profile_coverage) {
                        g.profile_coverage = parseFloat(g.profile_coverage).toFixed(2);
                    }
                    if (g.sequence_coverage) {
                        g.sequence_coverage = parseFloat(g.sequence_coverage).toFixed(2);
                    }
                }
                for (var j = 0; j < presence.length ; j++) {
                    var  p = presence[j];
                    var arr = $.map(list[i].summary[p], 
                                    function (value, key) {
                                        return {'name': key,
                                                'color': colorPicker.pick({'match': key}),
                                                'value': value };
                                    });
                    list[i].summary[p]=arr;
                }
            }
            callback();
        });
    };
    
    return {
        load: load,
        reset: reset,
        presence: presence,
        list: function () {
            return list;
        },
        isOrdered: function(){
            return isOrdered
        }
    };

}());
