import 'package:flutter/cupertino.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'global_configuration.dart';
import 'package:sprintf/sprintf.dart';
import 'package:apple_sign_in/apple_sign_in.dart';
import 'package:flutter/material.dart';


class LoginService extends ChangeNotifier {
  GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: [
      'email'
    ],
  );
  final String uidKey = "sportUID";
  String accountURL = "%s/account/";

  LoginService() {
    checkPrevLogin();
  }

  GoogleSignInAccount _user;
  int _uid;

  int get uid => _uid;

  GoogleSignInAccount get user => _user;

  String _generateURL(String extend, List<String> params) {
    params.insert(0, baseURL);
    var injectedURL = sprintf(extend, params);
    return injectedURL;
  }

  Future<void> logout() async {
    _uid = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    notifyListeners();
  }

  Future<void> checkPrevLogin() async {
    final prefs = await SharedPreferences.getInstance();
    _uid = prefs.getInt(uidKey);
    notifyListeners();
    print("reading: $_uid");
  }

  Future<void> _getUID(String guid) async {
    String guid2UID = _generateURL(accountURL, []);
    try {
      http.Response request = await http.post(guid2UID, body: jsonEncode({"GID": guid}));
      final data = json.decode(request.body);
      _uid = data["account"];
      final prefs = await SharedPreferences.getInstance();
      prefs.setInt(uidKey, _uid);
    } catch (error) {
      print("Error in getting uid");
    }
  }

  Future<void> handleIOSSignIn(BuildContext context) async {
    try {
      final AuthorizationResult result = await AppleSignIn.performRequests([AppleIdRequest(requestedScopes: [Scope.email])]);

      if (result.status == AuthorizationStatus.authorized) {
        print(result.credential.user);
        await _getUID(result.credential.user);
        notifyListeners();
      } else {
        throw Exception();
      }
    } catch (error) {
      loginError(context);
    }

  }

  Future<void> handleSignIn(BuildContext context) async {
    GoogleSignInAccount curUser;
    try {
      curUser = await _googleSignIn.signIn();
      _user = curUser;
      await _getUID(curUser.id);
      notifyListeners();
    } catch (error) {
      loginError(context);
    }
  }

  loginError(BuildContext context) {
    return showDialog(
        context: context,
        builder: (context) {
          return SimpleDialog(
            title: Text("Login Failure"),
            children: <Widget>[
              Text("Please try again.")
            ],
          );
        }
      );
  }
}