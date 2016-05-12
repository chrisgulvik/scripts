#!/usr/bin/env perl


use strict;
use Excel::Writer::XLSX;


die usage() if(@ARGV<1);
my $base = $ARGV[0];
$base =~ s{\.[^.]+$}{};

my $book=Excel::Writer::XLSX -> new("$base.xlsx");
my $sheet=$book -> add_worksheet('Sheet1');
my $row=0;

open(INPUT,$ARGV[0]);
while(<INPUT>){
    chomp;
    my @cells=split('\t',$_);
    my $col=0;
    for my $cell(@cells){
        $sheet -> write($row,$col,$cell);
        $col++ ;
    }
    $row++ ;
}
close INPUT;

sub usage{
"Converts a tab-delimited file into a Microsoft Excel spreadsheet.
Output is automatically created in same directory as the input.

usage: $0 <inputfile>
";
}
