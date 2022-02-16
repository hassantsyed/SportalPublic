import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';


class DefaultService extends ChangeNotifier {

  DefaultService() {
    checkDefault();
  }

  int _defaultSelection;

  int get defaultSelection => _defaultSelection;

  checkDefault() async {
    final prefs = await SharedPreferences.getInstance();
    var selection = prefs.getInt("defaultSelection");
    if (selection == null) {
      selection = 2;
      print("no selection, defaulting to 2");
    } else {
      print("selection set: $selection");
    }
    _defaultSelection = selection;
    notifyListeners();
  }

  setDefault(int selection) async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setInt("defaultSelection", selection);
    _defaultSelection = selection;
    notifyListeners();
  }
}