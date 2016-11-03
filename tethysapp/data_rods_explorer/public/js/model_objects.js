var MODEL_FENCES = null;
var MODEL1_LAYER = null;
var MODEL2_LAYER = null;
var VAR_DICT = null;
var DATARODS_TSB = null;
var DATARODS_PNG = null;
var WMS_VARS = null;
var COMPARE_TWO = false;

function setVarDict(varDictEncoded) {
    var varDictStr = varDictEncoded.replace(/&quot;/g, '"');
    VAR_DICT = JSON.parse(varDictStr);
}

function setModelFences(modelFencesEncoded) {
    var modelFencesStr = modelFencesEncoded.replace(/&quot;/g, '"');
    MODEL_FENCES = JSON.parse(modelFencesStr);
}

function setDataRodsPNG(dataRodsPNGEncoded) {
    var dataRodsPNGStr = dataRodsPNGEncoded.replace(/&quot;/g, '"');
    DATARODS_PNG = JSON.parse(dataRodsPNGStr);
}

function setDataRodsTSB(dataRodsTSBEncoded) {
    var dataRodsTSBStr = dataRodsTSBEncoded.replace(/&quot;/g, '"');
    DATARODS_TSB = JSON.parse(dataRodsTSBStr);
}

function setWMSVars(dataRodsTSBEncoded) {
    var dataRodsTSBStr = dataRodsTSBEncoded.replace(/&quot;/g, '"');
    WMS_VARS = JSON.parse(dataRodsTSBStr);
}