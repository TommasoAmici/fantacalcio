import {
  LEAGUE_CREATED,
  AUTH_ERROR,
  LEAGUE_SELECTED,
  LEAGUE_UPDATED
} from "./types";
import { errorHandler } from "./index";
import axios from "axios";

/*
 * Redux actions to handle leagues 
*/

function newLeague({ name }, history) {
  return function(dispatch) {
    axios
      .post(
        "/leagues/",
        { name, teams: [] },
        {
          headers: { Authorization: "JWT " + localStorage.getItem("user") }
        }
      )
      .then(response => {
        dispatch({
          type: LEAGUE_CREATED,
          payload: response.data
        });
        history.push("/dashboard/league-created");
      })
      .catch(error => {
        errorHandler(dispatch, error.response, AUTH_ERROR);
      });
  };
}

function joinLeague({ name, access_code, history }, browserHistory) {
  return function(dispatch) {
    axios
      .post(
        "/teams/",
        { name, access_code, history },
        {
          headers: { Authorization: "JWT " + localStorage.getItem("user") }
        }
      )
      .then(response => {
        dispatch({
          type: LEAGUE_CREATED,
          payload: response.data
        });
        browserHistory.push("/dashboard");
      })
      .catch(error => {
        errorHandler(dispatch, error.response, AUTH_ERROR);
      });
  };
}

function selectLeague(history) {
  return function(dispatch) {
    const accessCode = localStorage.getItem("league");
    axios
      .get("/leagues/" + accessCode + "/", {
        headers: { Authorization: "JWT " + localStorage.getItem("user") }
      })
      .then(response => {
        dispatch({
          type: LEAGUE_SELECTED,
          payload: {
            accessCode: accessCode,
            selected: true,
            name: response.data.name
          }
        });
        history.push("/dashboard");
      });
  };
}

function editLeague({ name, history, accessCode }) {
  return function(dispatch) {
    axios
      .put(
        "/leagues/" + accessCode + "/",
        { name, teams: [] },
        {
          headers: { Authorization: "JWT " + localStorage.getItem("user") }
        }
      )
      .then(response => {
        dispatch({
          type: LEAGUE_UPDATED,
          payload: {
            accessCode: accessCode,
            selected: true,
            name: response.data.name
          }
        });
      })
      .catch(error => {
        errorHandler(dispatch, error.response, AUTH_ERROR);
      });
  };
}

export { newLeague, joinLeague, selectLeague, editLeague };