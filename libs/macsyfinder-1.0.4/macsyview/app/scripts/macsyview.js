/*jslint plusplus: true */
/*global $, FileReader, Mustache, console, location, window */

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

var macsyview = (function () {
    'use strict';

    var go = function (hashString) {
        location.hash = "#!" + hashString;
        $(window).trigger('hashchange');
    },

        checkDataId = function () {
            // control that we are asking for the correct file
            var macsyviewRequestedId = parseInt(location.hash.split(":")[1], 10);
            if (macsyviewRequestedId !== macsyview.data.list().macsyviewId) {
                go('select');
                return false;
            } else {
                return true;
            }
        },
        
        init = function () {
            macsyview.view.init();
            $(window).bind('hashchange', function (event) {
                var viewName = location.hash.split(":")[0];
                switch (viewName) {
                case "#!select":
                    $("#listLink").hide();
                    macsyview.view.displaySelectForm();
                    break;
                case "#!list":
                    $("#listLink").hide();
                    $("#listLink").attr('href',location.hash);
                    checkDataId();
                    switch (location.hash.split(":")[2]) {
                    case "by_system":
                        macsyview.view.displaySystemMatches(['name', 'replicon.name', 'occurrence_number']);
                        break;
                    case "by_replicon":
                    default:
                        macsyview.view.displaySystemMatches(['replicon.name', 'name', 'occurrence_number']);  
                        break;
                    }
                    break;
                case "#!detail":
                    checkDataId();
                    $("#listLink").show();
                    var detailDoc = macsyview.data.list().filter(function(item){
                        return item.id==location.hash.split(":")[2];
                    })[0];
                    macsyview.view.displaySystemMatchFileDetail(detailDoc);
                    break;
                default:
                    go('select');
                }
            });
            $(window).trigger('hashchange');
        };

    return {
        init: init,
        go: go
    };
}());
