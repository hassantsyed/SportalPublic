import 'dart:convert';
import 'package:http/http.dart' as http;
import 'group.dart';
import 'GroupPick.dart';
import 'package:flutter/material.dart';
import 'package:sprintf/sprintf.dart';
import 'global_configuration.dart';

class GroupService extends ChangeNotifier {
  String pastGroupPickURL = "%s/crowd/past/%s/%s/";
  String listGroups = "%s/crowd/%s/";
  String createGroupURL = "%s/crowd/create/%s/";
  String joinGroupURL = "%s/crowd/add/%s/%s/";
  int uid;

  GroupService({@required this.uid});

  final List<Group> _groups = [];
  
  final List<GroupPick> _groupPicks = [];
  bool _loading = true;
  bool _fail = false;

  List<GroupPick> get groupPicks => _groupPicks;
  List<Group> get groups => _groups;

  bool get loading => _loading;
  bool get fail => _fail;

  String _generateURL(String extend, List<String> params) {
    params.insert(0, baseURL);
    var injectedURL = sprintf(extend, params);
    return injectedURL;
  }

  createGroup(String name) async {
    if (name == null) return;
    _fail = false;
    String requestURL = _generateURL(createGroupURL, [uid.toString()]);
    Map<String, String> createBody = {"name": name};
    String uuid;
    try {
      http.Response submitCreateGroup = await http.post(requestURL, body: jsonEncode(createBody));
      var createResp = jsonDecode(submitCreateGroup.body);
      var uuid = createResp["uuid"];
      await getGroups();
    } catch (ex, st) {
      _fail = true;
      print("request failed with ${ex.toString()}, with stacktrace: ${st.toString()}");
    }
    notifyListeners();
    return uuid;
  }

  joinGroup(String code) async {
    if (code == null) return;
    String requestURL = _generateURL(joinGroupURL, [code, uid.toString()]);
    try {
      _fail = false;
      http.Response resp = await http.get(requestURL);
      var res = json.decode(resp.body);
      if (res["status"] != 200) {
        _fail = true;
      }
      await getGroups();
    } catch (ex, st) {
      _fail = true;
      print("request failed with ${ex.toString()}, with stacktrace: ${st.toString()}");
    }
    notifyListeners();
  }

  getGroupPicks(String gid, int lid) async {
    _loading = true;
    notifyListeners();
    String requestURL = _generateURL(pastGroupPickURL, [gid, lid.toString()]);
    _groupPicks.clear();
    try {
      _fail = false;
      http.Response req = await http.get(requestURL);
      final data = json.decode(req.body);
      List<dynamic> datas = data["crowds"];
      for (var match in datas) {
        _groupPicks.add(GroupPick(match["mid"], 
          match["TEAM1"],
          match["TEAM2"], 
          match["player1"], 
          match["player2"], 
          match["winner"],
          DateTime.parse(match["date"]).toLocal()
          )
        );
      }
    } catch (ex, st) {
      _fail = true;
      print("request failed with ${ex.toString()}, with stacktrace: ${st.toString()}");
    }
    _loading = false;
    notifyListeners();
  }

  Future getGroups() async {
    String req = _generateURL(listGroups, [uid.toString()]);
    _groups.clear();
    try {
      _fail = false;
      var resp = await http.get(req);
      final data = json.decode(resp.body);
      
      for (var group in data["crowds"]) {
        _groups.add(Group(group["ooid"], group["name"]));
      }
    } catch (ex, st) {
      _fail = true;
      print("request failed with ${ex.toString()}, with stacktrace: ${st.toString()}");
    }
    notifyListeners();
  }

}
