//by CWHer
uses dos;
const date:array[1..12]of longint=(31,28,31,30,31,30,31,31,30,31,30,31);
  flin='settings.py';
  flout='temp.py';
  path='D:\Python\Pixiv\pixiv_crawl\';
  //path='D:\Test\backup\';
  year='2017';
var fin,fout:text;
  month,day:longint;
  line:ansistring;
  opt:char;

procedure work(var line:ansistring);
var idx_m,idx_d,endl:longint;
  m,d:ansistring;
begin
  idx_m:=0; idx_d:=0;
  str(month,m); str(day,d);
  if pos(year,line)=0 then exit();
  idx_m:=pos(year,line)+4;
  idx_d:=idx_m+1;
  while line[idx_d]<>',' do inc(idx_d);
  delete(line,idx_m+1,idx_d-idx_m-1);
  //writeln(line);
  insert(m,line,idx_m+1);
  //writeln(line);
  idx_d:=idx_m+1;
  while line[idx_d]<>',' do inc(idx_d);
  endl:=idx_d+1;
  while line[endl]<>')' do inc(endl);
  delete(line,idx_d+1,endl-idx_d-1);
  //writeln(line);
  insert(d,line,idx_d+1);
  //writeln(line);
end;

procedure strcre();
begin                             //new date
  //assign(fin,flin);
  //assign(fout,flout);
  assign(input,path+flin); reset(input);
  assign(output,path+flout); rewrite(output);
  while not eof do
   begin
    readln(line);
    work(line);
    writeln(line);
   end;
  close(input); close(output);
  //close(fin);
  //close(fout);
  erase(input);
end;

procedure strcpy();
begin                             //remake setting.py
  //assign(fin,flout);
  //assign(fout,flin);
  assign(input,path+flout); reset(input);
  assign(output,path+flin); rewrite(output);
  while not eof do
   begin
    readln(line);
    writeln(line);
   end;
  close(input); close(output);
  //close(fin);
  //close(fout);
  //erase(fin);
  erase(input);
end;

procedure run_crawler();
begin
  exec('main.bat','');
end;

begin
  repeat
   writeln('Start The Crawler?(Y\N)');
   readln(opt);
   opt:=lowercase(opt);
  until opt in ['y','n'];
  if opt='n' then halt();
  for month:=1 to 12 do
   for day:=1 to date[month] do
    begin
     strcre();
     strcpy();
     run_crawler();
    end;
end.

