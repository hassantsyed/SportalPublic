import 'dart:collection';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:sportbook/GroupPick.dart';
import 'package:sportbook/empty_card.dart';
import 'group_service.dart';
import 'stat_card.dart';
import 'admob_service.dart';

class GroupStats extends StatelessWidget {
  final ams = AdMobService();
  
  _buildStatCard(int i, GroupPick groupPick) {
    return StatCard(groupPick: groupPick, key: ValueKey(groupPick));
  }

  _buildExtension(int idx, List<GroupPick> groupPicks) {
    var titleDate = "${groupPicks[0].date.year.toString()}-${groupPicks[0].date.month.toString()}-${groupPicks[0].date.day.toString()}";
    return Card(
      child: ExpansionTile(
        initiallyExpanded: false,
        title: Text(titleDate),
        children: <Widget>[
          ListView.builder(
            shrinkWrap: true,
            itemCount: groupPicks.length * 2,
            itemBuilder: (context, index) {
              if (index.isOdd) return Divider();

              final idx = index ~/ 2;

              return _buildStatCard(idx, groupPicks[idx]);
            },
            physics: ScrollPhysics(),
          ),
        ],
      )
    );
  }

  statList(GroupService groupService) {
    if (groupService.loading) {
      return Center(
        child: CircularProgressIndicator()
      );
    }
    if (groupService.groupPicks.length == 0) {
      if (groupService.fail) {
        return EmptyCard(emptyText: "Unable to get group stats. Pleae Retry.");
      }
      return EmptyCard(emptyText: "No Group Stats Yet");
    }
    LinkedHashMap<String, List<GroupPick>> dateMatches = LinkedHashMap();
    List<List<GroupPick>> dateOrderedMatches = List();
    groupService.groupPicks.forEach((element) {
      String dateKey = "${element.date.year.toString()}-${element.date.month.toString()}-${element.date.day.toString()}";
      if (dateMatches.containsKey(dateKey)) {
        dateMatches[dateKey].add(element);
      } else {
        dateMatches[dateKey] = [element];
      }
    });
    dateMatches.forEach((key, value) {
      dateOrderedMatches.add(value);
    });

    int extensionCount = dateOrderedMatches.length;
    return ListView.builder(
      itemCount: extensionCount,
      itemBuilder: (context, index) {
        return _buildExtension(index, dateOrderedMatches[index]);
      },
    );
    // return ListView.builder(
    //   itemCount: groupService.groupPicks.length*2,
    //   itemBuilder: (context, index) {
    //     if (index.isOdd) return Divider();
    //     final idx = index ~/ 2;
    //     return _buildStatCard(groupService.groupPicks[idx]);
    //   },
    // );
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<GroupService>(
      builder: (context, groupService, child) {
        return Scaffold(
          body: statList(groupService)
        );
      },
    );
  }
}