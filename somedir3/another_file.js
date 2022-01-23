const Discord = require("discord.js");
const intents = new Discord.Intents(0b111111111111111);
const client = new Discord.Client({ intents: intents });

client.commands = new Discord.Collection();
client.rankServerCommands = new Discord.Collection();

const prefix = '.';

const fs = require('fs');

const Permission = require('./data/Permission');

const Inko = require('inko');
const inko = new Inko();

// client.rankServerCommands setting
for (const file of fs.readdirSync('./rankServerCommands')) {
  const cmd = require(`./rankServerCommands/${file}`);
  client.rankServerCommands.set(cmd.id, cmd);
}

// client.commands setting
for (const folder of fs.readdirSync('./commands')) {
  for (const file of fs.readdirSync(`./commands/${folder}`)) {
    const cmd = require(`./commands/${folder}/${file}`);
    client.commands.set(cmd.name.join(' '), cmd);
  }
}

client.log = async (...s) => {
  let logmsg = s.join('\n');
  console.log(logmsg.slice(0, 2000));
  await client.channels.cache.get('883236535854571590').send(logmsg.slice(0, 2000));

  if (logmsg.slice(2000)) {
    await client.log(logmsg.slice(2000));
  }
}

client.BGJ_log = async (...s) => {
  let logmsg = s.join('\n');
  console.log(logmsg.slice(0, 2000));
  await client.channels.cache.get('907230087655620608').send(logmsg.slice(0, 2000));

  if (logmsg.slice(2000)) {
    await client.BGJ_log(logmsg.slice(2000));
  }
}


client.ERROR_catched = async (e, message=null) => {
  await client.log('ERROR!(<@!526889025894875158>)...', '```js', '<name>', e.name, '<message>', e.message, '<stack>', e.stack, '```');
  if (message) client.log('`in`', message.guild.name, message.channel.name, message.url);
}

client.BGJ_ERROR_catched = async (e, message=null) => {
  await client.BGJ_log('ERROR!(<@!526889025ㅓ어아 핑하지마ㅏ세오894875158>)...', '```js', '<name>', e.name, '<message>', e.message, '<stack>', e.stack, '```');
  if (message) client.BGJ_log('`in`', message.guild.name, message.channel.name, message.url);
}



client.on("ready", async () => {
  try {

    await client.log('<@!526889025894875158>', client.user.tag, 'online!');

  } catch (e) { await client.ERROR_catched(e); }
});

client.on("messageCreate", async (message) => {
  try {

    // 답장핑 끄기 및 기타 message.reply 재정의
    message.reply_ = message.reply;
    message.reply = async (s) => {
      if (typeof s === 'string') { // s가 문자열일때 처리
        if (!s.trim().length) s = '말을 할수 없는 (비어있음)'; // 비어있을때 기본값
        if (s.length > 2000) s = `말을 할수 없는 (너무 긺, ${s.length}글자)` // 너무 길때 기본값
      }
      let inputObj = typeof s === 'string' ? {content: s} : s;
      let sourceObj = {
        allowedMentions: {
          users: [message.author.id],
          repliedUser: false
        }
      }
      let resultObj = Object.assign(inputObj, sourceObj);
      return await message.reply_(resultObj);
    }

    // 메시지 분류
    // 1. 랭크 서버
    // if (message.guildId === 766932314973929522) {
    //   const MC = message.content;
    //   const MAI = message.authorId;
    //   const MCI = message.channelId;

    //   const isStart = (s) => MC.startsWith(s);
    //   const Admins = ['647001590766632966', '725528129648721920', '436071996661563402']; // 생강, 내려놔, 키기루
    //   const isAdmin = () => Admins.includes(MAI);
    //   const RankUpChannels = ['766932314973929527', '783516524685688842', '871400280854523905'];
    //   const isRankUpChannel = () => RankUpChannels.includes(MCI);
    //   const BettingChannels = ['784228694940057640', '794146499034480661'];
    //   const isBettingChannel = () => BettingChannels.includes(MCI);

    //   const cmd = (() => {
    //     if (( isStart(',+') || isStart(',-') ) && isAdmin()) {
    //       return client.rankServerCommands.get(1);
    //     } else if (isRankUpChannel()) {
    //       return client.rankServerCommands.get(2);
    //     } else if (isBettingChannel()) {
    //       return client.rankServerCommands.get(3);
    //     } else if (isStart(',일급') && isAdmin()) {
    //       return client.rankServerCommands.get(4);
    //     }
    //   })();

    //   if (!cmd) return; // 커맨드가 감지되지 않음

    //   const inputData = {
    //     client: client,
    //     message: message,
    //   }

    //   if (cmd) await cmd.run(inputData);
    // }

    // 2. 그 외
    if (message.content.startsWith(prefix)){
      let Ms_ = message.content.slice(prefix.length).split(' '); // 매개변수 목록, 명령어 포함

      let cmd = client.commands.find(command => {
        let userUse = Ms_.slice(0, command.name.length);
        return command.name.map(inko.ko2en).join(' ') === userUse.map(inko.ko2en).join(' ');
      });

      if (!cmd) return; // 커맨드가 감지되지 않음

      Ms_ = Ms_.slice(cmd.name.length);


      const checkPermissionData = {
        message: message,
      }

      if ( Permission.data[cmd.permission](checkPermissionData) ) {
        // Ms 생성
        let Ms;
        let my_number = Ms_.length;
        let can_numbers = [...cmd.MsLength]; // 복사
        if (!can_numbers.at(-1)) { // 가능한 수중 가장 큰수가 0, 매개변수가 필요없음
          Ms = [];
        } else if (my_number < can_numbers[0]) { // 가능한 수중 가장 작은수보다도 더 작음, "적음"
          await message.reply(`매개변수가 부족합니다. 최소 ${can_numbers[0]}개의 매개변수가 필요하지만, ${my_number}개의 매개변수가 입력되었습니다. \`.도움 ${cmd.name.join(' ')}\`(으)로 자세한 도움말을 확인할 수 있습니다.`);
          return;
        } else { // 정상적인 상황.
          const final_number = [...can_numbers].reverse().find( i => (i <= my_number) ); // 가능한 수중 주어진 매개변수의 수보다 작은 수중 최댓값. (사용할 매개변수의 수)
          Ms = [ ...Ms_.slice(0, final_number-1), Ms_.slice(final_number-1).join(' ') ];
        }

        const inputData = {
          client: client,
          message: message,
          Ms: Ms,
        }

        await cmd.run(inputData);
      }

    }

  } catch(e) { await client.ERROR_catched(e, message); }
});

const token = process.env.TOKEN;
client.login(token);
//TODO - Putting hyphen as test and I think this class should be careful of open connections.