var MODEL_FENCES = null;
var MODEL1_LAYER = null;
var MODEL2_LAYER = null;
var VAR_DICT = null;
var COMPARE_TWO = false;

function setVarDict(varDictEncoded) {
    var varDictStr = varDictEncoded.replace(/&quot;/g, '"');
    VAR_DICT = JSON.parse(varDictStr);
}

function setModelFences(modelFencesEncoded) {
    var modelFencesStr = modelFencesEncoded.replace(/&quot;/g, '"');
    MODEL_FENCES = JSON.parse(modelFencesStr);
}