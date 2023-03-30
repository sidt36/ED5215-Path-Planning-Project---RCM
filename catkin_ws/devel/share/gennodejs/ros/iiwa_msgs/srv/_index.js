
"use strict";

let SetEndpointFrame = require('./SetEndpointFrame.js')
let SetPTPJointSpeedLimits = require('./SetPTPJointSpeedLimits.js')
let ConfigureControlMode = require('./ConfigureControlMode.js')
let SetSmartServoLinSpeedLimits = require('./SetSmartServoLinSpeedLimits.js')
let SetPTPCartesianSpeedLimits = require('./SetPTPCartesianSpeedLimits.js')
let TimeToDestination = require('./TimeToDestination.js')
let SetWorkpiece = require('./SetWorkpiece.js')
let SetSpeedOverride = require('./SetSpeedOverride.js')
let SetSmartServoJointSpeedLimits = require('./SetSmartServoJointSpeedLimits.js')

module.exports = {
  SetEndpointFrame: SetEndpointFrame,
  SetPTPJointSpeedLimits: SetPTPJointSpeedLimits,
  ConfigureControlMode: ConfigureControlMode,
  SetSmartServoLinSpeedLimits: SetSmartServoLinSpeedLimits,
  SetPTPCartesianSpeedLimits: SetPTPCartesianSpeedLimits,
  TimeToDestination: TimeToDestination,
  SetWorkpiece: SetWorkpiece,
  SetSpeedOverride: SetSpeedOverride,
  SetSmartServoJointSpeedLimits: SetSmartServoJointSpeedLimits,
};
