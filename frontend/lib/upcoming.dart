import 'dart:collection';

import 'package:flutter/material.dart';
import 'package:sportbook/match_service.dart';
import 'match.dart';
import 'upcoming_card.dart';
import 'package:provider/provider.dart';
import 'empty_card.dart';
import 'admob_service.dart';

class Upcoming extends StatelessWidget {
  final ams = AdMobService();

  _buildRow(int i, Match match) {
    return UpcomingCard(match: match, key: ObjectKey(match));
  }

  _buildExtension(int idx, List<Match> matches) {
    var titleDate = "${matches[0].date.year.toString()}-${matches[0].date.month.toString()}-${matches[0].date.day.toString()}";
    return Card(
      child: ExpansionTile(
        initiallyExpanded: true,
        title: Text(titleDate),
        children: <Widget>[
          ListView.builder(
            shrinkWrap: true,
            itemCount: matches.length * 2,
            itemBuilder: (context, index) {
              if (index.isOdd) return Divider();

              final idx = index ~/ 2;

              return _buildRow(index, matches[idx]);
            },
            physics: ScrollPhysics(),
          ),
        ],
      )
    );
  }

  upcomingList(MatchService matchService) {
    if (matchService.loading) {
      return Center(
        child: CircularProgressIndicator()
      );
    }
    if (matchService.matches.length == 0) {
      if (matchService.fail) {
        return EmptyCard(emptyText: "Unable to get upcoming matches. Please retry.");
      } else {
        return EmptyCard(emptyText: "No Upcoming Events");
      }
    }
    LinkedHashMap<String, List<Match>> dateMatches = LinkedHashMap();
    List<List<Match>> dateOrderedMatches = List();
    matchService.matches.forEach((element) {
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
        return _buildExtension(index, dateOrderedMatches[(extensionCount-1)-index]);
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<MatchService>(
      builder: (context, matchService, child) {
        return Scaffold(
          body: upcomingList(matchService)
        );
      },
    );
  }
}