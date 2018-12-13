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
 * macsyview.view
 * view module for macsyview
 */

/* jslint   browser : true, continue : true,
  devel  : true, indent  : 4,    maxerr   : 50,
  newcap : true, nomen   : true, plusplus : true,
  regexp : true, sloppy  : true, vars     : false,
  white  : true
 */

/*global $, macsyview, Mustache, console*/

macsyview.view = (function () {
    'use strict';

    var config = {
        viewContainer: "#mainView",
        directory: "#directory",
        homeLink: "#homeLink",
        systemMatchesLinkList: "#systemMatchesLinkList"
    },

        viewContainer = $(config.viewContainer),

        displayWaitSplash = function (toggle) {
            $('#waitMessage').toggleClass('in', toggle);
            $('#waitBack').toggleClass('in', toggle);
            var displayValue = toggle ? 'block' : 'none';
            $('#waitMessage').css('display', displayValue);
            $('#waitBack').css('display', displayValue);
        },
        
        displayView = function (viewName, context) {
            viewContainer.html('');
            var template = $('#' + viewName).text();
            viewContainer.html(Mustache.render(template, context));
        },

        pathValue = function (obj, path, defaultValue) {
            var properties = path.split('.'),
                i;
            for (i = 0; i < properties.length; i++) {
                if (!obj) {
                    return defaultValue || null;
                }
                obj = obj[properties[i]];
            }
            return obj || defaultValue;
        },

        sortByKeys = function (keys) {
            return function (item1, item2) {
                var cmpRes = 0,
                    keysHere = keys.slice(),
                    currentKey;
                while (cmpRes === 0 && keysHere.length > 0) {
                    currentKey = keysHere.shift();
                    var i1 = pathValue(item1, currentKey, '');
                    var i2 = pathValue(item2, currentKey, '');                    
                    if (typeof i1 =="number"){
                        // compare numeric values
                        if(i1 <i2){
                            cmpRes = -1;
                        }else if(i1 == i2){
                            cmpRes = 0;
                        }else if(i1 > i2){
                            cmpRes = 1;
                        }
                    }else{
                        // compare string values
                        cmpRes = i1.localeCompare(i2);
                    }
                }
                return cmpRes;
            };
        },

        displaySystemMatchFileDetail = function (doc) {
            displayView('systemMatchDetail', doc);
            macsyview.system.init(doc, "system_schema");
            if(macsyview.data.isOrdered()){
                $("#genomicContextPanel").removeClass("hidden");
                macsyview.orderedview.draw(doc, "replicon_schema");
            }
        },

        initSystemMatchSelectionHandler = function () {
            $(config.viewContainer + " .txsview-systemmatchtablerow td").click(function (e) {
                var id = $(e.currentTarget).parent().attr('data-systemmatchid');
                macsyview.go('detail:' + macsyview.data.list().macsyviewId + ":" + id);
            });
        },

        displaySystemMatches = function (sortKeys) {
            displayWaitSplash(true);
            var list = macsyview.data.list();
            list.sort(sortByKeys(sortKeys));
            var tplData = {
                'files': list,
                'sortKey': sortKeys[0],
            };
            switch (sortKeys[0]) {
            case "replicon.name":
                tplData["sortBySystemLink"] = "list:" + macsyview.data.list().macsyviewId + ":by_system";
                break;
            case "name":
                tplData["sortByRepliconLink"] = "list:" + macsyview.data.list().macsyviewId + ":by_replicon";
                break;
            }
            var tplName = macsyview.data.isOrdered() ? 'systemMatchesOrderedList' : 'systemMatchesUnorderedList';
            displayView(tplName, tplData);
            initSystemMatchSelectionHandler();
            displayWaitSplash(false);
        },

        fileSelectionHandler = function (e) {
            displayWaitSplash(true);
            var jsonFile = e.target.files[0];
            macsyview.data.load(jsonFile, function () {
                macsyview.go("list:" + macsyview.data.list().macsyviewId + ":by_replicon");
                displayWaitSplash(false);
            });
        },

        displaySelectForm = function () {
            $(config.systemMatchesLinkList).hide();
            displayView('runSelectForm', {});
            $(config.directory).change(fileSelectionHandler);
        },

        init = function () {
            $(config.homeLink).click(displaySelectForm);
            $(config.systemMatchesLinkList).click(displaySystemMatches);
            displaySelectForm();
        };

    return {
        'config': config,
        'init': init,
        'displaySelectForm': displaySelectForm,
        'displaySystemMatches': displaySystemMatches,
        'displaySystemMatchFileDetail': displaySystemMatchFileDetail
    };

}());