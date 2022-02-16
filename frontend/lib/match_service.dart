import 'dart:convert';
import 'package:http/http.dart' as http;
import 'match.dart';
import 'team.dart';
import 'pick.dart';
import 'package:flutter/material.dart';
import 'package:sprintf/sprintf.dart';
import 'global_configuration.dart';

class MatchService extends ChangeNotifier {
  String upcomingMatchURL = "%s/match/upcoming/%s";
  String pastMatchURL = "%s/match/finished/%s";
  String upcomingPickURL = "%s/pick/current/%s/%s/";
  String pastPickURL = "%s/pick/past/%s/%s/";
  String submitPickURL = "%s/pick/upsert/%s/%s/";

  int uid;

  MatchService({@required this.uid});

  final List<Match> _matches = [];
  bool _loading = true;
  bool _fail = false;

  List<Match> get matches => _matches;
  bool get loading => _loading;
  bool get fail => _fail;

  String _generateURL(String extend, List<String> params) {
    params.insert(0, baseURL);
    var injectedURL = sprintf(extend, params);
    return injectedURL;
  }

  Future<List<Match>> getMatches(Status state, int lid) async {
    String requestURL;
    switch(state) {
      case Status.upcoming:
      {
        requestURL = upcomingMatchURL;
      }
      break;
      case Status.finished:
      {
        requestURL = pastMatchURL;
      }
      break;
    }
    requestURL = _generateURL(requestURL, [lid.toString()]);

    List<Match> matches = [];
    try {
      http.Response request = await http.get(requestURL);
      final data = json.decode(request.body);
      List<dynamic> datas = data["matches"];
      for (var matchData in datas) {
        var t1 = new Team(matchData["team1"]["name"]);
        var t2 = new Team(matchData["team2"]["name"]);
        matches.add(new Match(matchData["MID"], matchData["LID"], t1, t2, matchData["status"], DateTime.parse(matchData["date"]).toLocal(), matchData["result"]));
      }
      _fail = false;
    } catch (ex, st) {
      _fail = true;
      print("request failed with ${ex.toString()}, with stacktrace: ${st.toString()}");
    }

    return matches;
  }

  Future<List<Pick>> getPicks(Status state, int lid) async {
    String requestURL;
    switch(state) {
      case Status.upcoming:
      {
        requestURL = upcomingPickURL;
      }
      break;
      case Status.finished:
      {
        requestURL = pastPickURL;
      }
    }

    List<Pick> picks = [];
    requestURL = _generateURL(requestURL, [uid.toString(), lid.toString()]);

    try {
      http.Response request = await http.get(requestURL);
      final data = json.decode(request.body);
      List<dynamic> datas = data["picks"];
      

      for (var pick in datas) {
        var p = Pick(pick["matchDetails"]["MID"], pick["pick"]);
        picks.add(p);
      }
      _fail = false;
    } catch (ex, st) {
      _fail = true;
      print("request failed with ${ex.toString()}, with stacktrace: ${st.toString()}");
    }

    return picks;
  }

  Future getMatchesWithPicks(Status state, int lid) async {
    _loading = true;
    notifyListeners();
    var picksAsync = getPicks(state, lid);
    var matchesAsync = getMatches(state, lid);
    var picks = await picksAsync;
    var matches = await matchesAsync;
    Map<int, Match> result = {};
    matches.forEach((match) {
      result[match.mid] = match;
    });
    picks.forEach((pick) {
      if (result[pick.mid] != null) {
        result[pick.mid].pick = pick.pick;
      }
    });
    
    _matches.clear();
    _matches.addAll(matches);
    _loading = false;
    notifyListeners();
  }

  void submitPick(Match match, int pick) async
  {
    match.loading = true;
    String requestURL = _generateURL(submitPickURL, [uid.toString(), match.mid.toString()]);

    Map<String, int> selectionBody = {"selection": pick};

    try {
      http.Response submitPick = await http.post(requestURL, body: jsonEncode(selectionBody));

      var selectionResp = jsonDecode(submitPick.body);
      if (selectionResp["status"] == 200) {
        if (pick == -1) {
          match.pick = null;
        } else if (pick == 0) {
          match.pick = "TEAM1";
        } else {
          match.pick = "TEAM2";
        }
      } else {
        print("Submit pick failed.");
      }
      match.loading = false;
      match.fail = false;
      notifyListeners();
    } catch (ex, st) {
      match.fail = true;
      match.loading = false;
      print("request failed with ${ex.toString()}, with stacktrace: ${st.toString()}");
    }
  }


}

enum Status {
  upcoming,
  finished
}