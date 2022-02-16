import 'package:admob_flutter/admob_flutter.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:sportbook/group_stats.dart';
import 'package:sportbook/league_model.dart';
import 'package:sportbook/login_service.dart';
import 'package:sportbook/match_service.dart';
import 'package:sportbook/group_service.dart';
import 'upcoming.dart';
import 'history.dart';
import 'admob_service.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';
import 'package:flutter_speed_dial/flutter_speed_dial.dart';
import 'default_service.dart';

class BottomTabs extends StatefulWidget {
  final selection;
  BottomTabs(this.selection);
  @override
  _BottomTabsState createState() => _BottomTabsState(selection);
}

class _BottomTabsState extends State<BottomTabs> with SingleTickerProviderStateMixin {
  List<LeagueModel> leagues = [
    LeagueModel(2, "UFC", Icon(MdiIcons.mixedMartialArts, color: Colors.white)),
    LeagueModel(1, "NBA", Icon(MdiIcons.basketballHoopOutline, color: Colors.white)),
    LeagueModel(3, "NFL", Icon(MdiIcons.footballHelmet, color: Colors.white)),
    // LeagueModel(4, "NHL", Icon(MdiIcons.hockeyPuck, color: Colors.white))
  ];
  TabController controller;
  int index = 0;
  int lid;
  Status curState = Status.upcoming;
  String groupID = "0000";
  final ams = AdMobService();
  AdmobBanner banner;
  List<Widget> _widgets = [Upcoming(), History()];

  _BottomTabsState(this.lid);
  

  @override
  void initState() {
    super.initState();
    Admob.initialize(ams.getAdMobAppId());
    banner = AdmobBanner(adUnitId: ams.getUpcomingAdId(), adSize: AdmobBannerSize.FULL_BANNER,);
  }

  void tapped(int tappedIdx) {
    Status newState;
    if (tappedIdx ==  0) {
      newState = Status.upcoming;
      Provider.of<MatchService>(context, listen: false).getMatchesWithPicks(newState, lid);
    } else if (tappedIdx == 1) {
      newState = Status.finished;
      if (groupID == "0000") {
        Provider.of<MatchService>(context, listen: false).getMatchesWithPicks(newState, lid);
      } else {
        Provider.of<GroupService>(context, listen: false).getGroupPicks(groupID, lid);
      }
    }
    setState(() {
      curState = newState;
      index = tappedIdx;
    });
  }

  showJoinCode(BuildContext context) {
    return showDialog(
      context: context,
      builder: (context) {
        return SimpleDialog(
          title: Text("Join Code"),
          children: <Widget>[
            SimpleDialogOption(
              child: (groupID != "0000") ? SelectableText(groupID) : Text("Group Not Selected") 
            )
          ],
        );
      }
    );
  }

  Future<List<String>> createGroupDialog(BuildContext context) {
    TextEditingController namecontroller = TextEditingController();
    TextEditingController codeController = TextEditingController();
    return showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text("Join/Create Group"),
          content: Column(
            children: <Widget>[
              TextField(
                controller: namecontroller,
                decoration: InputDecoration(
                  hintText: "New Group Name"
                ),
              ),
              TextField(
                controller: codeController,
                decoration: InputDecoration(
                  hintText: "Join Code"
                ),
              )
            ],
          ) 
          ,
          actions: <Widget>[
            MaterialButton(
              elevation: 5.0,
              child: Text("Join Group"),
              onPressed: () {
                Navigator.of(context).pop(["false", codeController.text.toString()]);
              },
            ),
            MaterialButton(
              elevation: 5.0,
              child: Text("Create Group"),
              onPressed: () {
                Navigator.of(context).pop(["true", namecontroller.text.toString()]);
              },
            )
          ],
        );
      }
    );
  }

  makeSnackbar(BuildContext context, String msg, Color color) {
    SnackBar snack = SnackBar(
      content: Text(msg),
      backgroundColor: color,
    );
    Scaffold.of(context).showSnackBar(snack);
  }

  List<SpeedDialChild> genSpeedDial() {
    List<SpeedDialChild> speedDial = [];
    leagues.forEach((league) {
      speedDial.add(
        SpeedDialChild(
          label: league.name,
          child: league.icon,
          onTap: () {
            setState(() {
              lid = league.lid;
            });
            tapped(index);
          }
        )
      );
    });
    return speedDial;
  }

  List<Widget> genListMenu() {
    List<Widget> listMenu = [];
    leagues.forEach((league) {
      bool chosen = Provider.of<DefaultService>(context, listen: false).defaultSelection == league.lid;
      listMenu.add(
        ListTile(
          title: Text(league.name),
          trailing: IconButton(
            icon: Icon(chosen ? Icons.favorite : Icons.favorite_border, size: 20, color: Colors.black,),
            onPressed: () {
              Provider.of<DefaultService>(context, listen: true).setDefault(league.lid);
            },
          ),
          onTap: () {
            setState(() {
              lid = league.lid;
            });
            tapped(index);
            Navigator.of(context).pop();
          }
        )
      );
      listMenu.add(Divider());
    });
    return listMenu;
  }

  SpeedDial makeSpeedDial() {
    return SpeedDial(
      animatedIcon: AnimatedIcons.menu_close,
      children: genSpeedDial(),
      marginBottom: 75,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text("Sportal"),
          actions: <Widget>[
            IconButton(
              onPressed: () {
                showJoinCode(context);
              },
              icon: Icon(Icons.info_outline),
            ),
            IconButton(
              icon: Icon(Icons.add_circle_outline),
              onPressed: () async {
                var data = await createGroupDialog(context);
                if (data == null || data[1] == null || data[1].trim() == "") {
                  makeSnackbar(context, "Input is invalid.", Colors.deepOrange);
                  return;
                }
                data[1] = data[1].trim();
                if (data[0] == "true") {
                  await Provider.of<GroupService>(context, listen: false).createGroup(data[1]);
                  if (Provider.of<GroupService>(context, listen: false).fail) {
                    makeSnackbar(context, "Unable to create group: ${data[1]}. Please retry.", Colors.deepOrange);
                  } else {
                    makeSnackbar(context, "Created group: ${data[1]}.", Colors.lightGreen);
                  }
                } else {
                  await Provider.of<GroupService>(context, listen: false).joinGroup(data[1]);
                  if (Provider.of<GroupService>(context, listen: false).fail) {
                    makeSnackbar(context, "Unable to join group: ${data[1]}. Please retry.", Colors.deepOrange);
                  } else {
                    makeSnackbar(context, "Joined group: ${data[1]}.", Colors.lightGreen);
                  }
                }
              },
            ),
            DropdownButton<String>(
              style: TextStyle(color: Colors.white),
              dropdownColor: Colors.blue,
              value: groupID,
              items: [DropdownMenuItem(
                value: "0000",
                child: Text("Self")
              )] + Provider.of<GroupService>(context).groups.map((e) {
                return DropdownMenuItem(
                  value: e.uuid,
                  child: Text(e.name)
                );
              }).toList(),
              onChanged: (String newVal) {
                if (newVal != "0000") {
                  Provider.of<GroupService>(context, listen: false).getGroupPicks(newVal, lid);
                } else {
                  Provider.of<MatchService>(context, listen: false).getMatchesWithPicks(curState, lid);
                }
                setState(() {
                  if (newVal == "0000") {
                    _widgets[1] = History();
                  } else {
                    _widgets[1] = GroupStats();
                  }
                  groupID = newVal;
                });
              },
            ),
          ],
        ),
        drawer: Drawer(
          child: ListView(
            padding: EdgeInsets.zero,
            children: <Widget>[
              SizedBox(
                height: 100,
                child: DrawerHeader(
                  decoration: BoxDecoration(
                    color: Colors.blue
                  ),
                  child: Text(
                    "League",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 24
                    )
                  )
                )
              ),
              ...genListMenu(),
              ListTile(
                title: Text("Logout"),
                onTap: () {
                  Provider.of<LoginService>(context, listen: false).logout();
                  Navigator.of(context).pop();
                }
              ),
              Divider()
            ]
          )
        ),
        body: Container(
          margin: EdgeInsets.only(bottom: 60),
          child: RefreshIndicator(
            child: _widgets[index],
            onRefresh: () async {
              if (index ==  0) {
                await Provider.of<MatchService>(context, listen: false).getMatchesWithPicks(curState, lid);
              } else {
                if (groupID == "0000") {
                  await Provider.of<MatchService>(context, listen: false).getMatchesWithPicks(curState, lid);
                } else {
                  await Provider.of<GroupService>(context, listen: false).getGroupPicks(groupID, lid);
                }
              }
            },
          ),
        ),
        floatingActionButton: makeSpeedDial(),
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: index,
          onTap: tapped,
          items: [
            BottomNavigationBarItem(
              icon: new Icon(Icons.assistant_photo), title: Text("Upcoming"),
            ),
            BottomNavigationBarItem(
              icon: new Icon(Icons.assessment), title: (groupID == "0000") ? Text("History"): Text("Stats"),
            )
          ],
        ),
        bottomSheet: banner
      );
  }
}