import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:sportbook/default_service.dart';
import 'package:sportbook/group_service.dart';
import 'match_service.dart';
import 'bottom_tabs.dart';
import 'package:flutter_auth_buttons/flutter_auth_buttons.dart';
import 'login_service.dart';
import 'dart:io';
import 'package:apple_sign_in/apple_sign_in.dart' as apple;

class LandingPage extends StatelessWidget {

  _determineButton(BuildContext context, bool appleSignInAvailable) {
    List<Widget> signInButtons = [];

    signInButtons.add(
      GoogleSignInButton(
        darkMode: true,
        onPressed: () {
          Provider.of<LoginService>(context, listen: true).handleSignIn(context);
        }
      )
    );

    if (Platform.isIOS && appleSignInAvailable) {
      signInButtons.add(
        apple.AppleSignInButton(
          style: apple.ButtonStyle.black,
          onPressed: () {
            Provider.of<LoginService>(context, listen: true).handleIOSSignIn(context);
          },
        )
      );
    }

    return Scaffold(
      appBar: AppBar(title: Text("Login")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: signInButtons,
        )
      )
    );
  }

  _determineAuth(BuildContext context, int uid, int selection) {
    bool passAuth = uid != null && selection != null;
    if (passAuth) {
      return MultiProvider(
        providers: [
          ChangeNotifierProvider<MatchService>(create: (context) {
            var matchService = MatchService(uid: uid);
            matchService.getMatchesWithPicks(Status.upcoming, selection);
            return matchService;
          },),
          ChangeNotifierProvider<GroupService>(create: (context) {
            var groupService = GroupService(uid: uid);
            groupService.getGroups();
            return groupService;
          },)
        ],
        child: Scaffold(
          body: BottomTabs(selection),
        )
      );
    }
    else {
      return FutureBuilder<bool>(
        future: apple.AppleSignIn.isAvailable(),
        builder: (context, AsyncSnapshot<bool> snapshot) {
          if (snapshot.hasData) {
            return _determineButton(context, snapshot.data);
          } else {
            return CircularProgressIndicator();
          }
        },
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Consumer2<LoginService, DefaultService>(
      builder: (context, loginService, defaultService, child) {
        return _determineAuth(context, loginService.uid, defaultService.defaultSelection);
      },
    );
  }
}