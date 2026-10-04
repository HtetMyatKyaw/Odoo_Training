# Training Tasks — ပထမဆုံး Odoo module

ဒီ module က Task အမည်၊ ရှင်းလင်းချက်၊ နောက်ဆုံးရက်နဲ့ လုပ်ငန်းအဆင့်ကို သိမ်းနိုင်တဲ့ သင်ခန်းစာ app ဖြစ်ပါတယ်။ Odoo 19 အတွက် ရေးထားပါတယ်။

## ၁။ Module ကို Odoo တွေ့နိုင်အောင်လုပ်ခြင်း

`config/odoo.conf` ရဲ့ `addons_path` ထဲမှာ ဒီ project ရဲ့ `Addons` directory ပါပြီးသားဖြစ်ပါတယ်။ Odoo ကို ဒီ config ဖြင့် run ရပါမယ်။

## ၂။ ဖိုင်တွေကို လေ့လာခြင်း

- `__manifest__.py` — module အမည်၊ Odoo dependency နဲ့ load လုပ်မယ့် CSV/XML ဖိုင်များကို သတ်မှတ်ပါတယ်။
- `__init__.py` နဲ့ `models/__init__.py` — Python model ကို Odoo ထံ import လုပ်ပေးပါတယ်။
- `models/training_task.py` — `training.task` model (database ထဲက task records)၊ တာဝန်ခံ user နဲ့ အဆင့် (`Draft → In Progress → Done`) ကို သတ်မှတ်ပါတယ်။ `name` မဖြစ်မနေ ဖြည့်ရပါတယ်။
- `security/ir.model.access.csv` — အတွင်းသုံး Odoo user များကို task ဖတ်၊ ဖန်တီး၊ ပြင်၊ ဖျက် ခွင့်ပြုပါတယ်။
- `views/training_task_views.xml` — task စာရင်း၊ ဖောင်၊ menu နဲ့ menu ဖွင့်မယ့် action ကို ဖန်တီးပါတယ်။
- `wizard/quick_task_wizard.py` — ခဏသုံး popup form (`TransientModel`) မှ Task အသစ်ဖန်တီးပါတယ်။ Wizard record က ယာယီဖြစ်ပြီး ဖန်တီးလိုက်တဲ့ Task က ပုံမှန် record ဖြစ်ပါတယ်။

## ၃။ Install လုပ်ခြင်း

Odoo server ပိတ်ထားချိန်မှာ project root မှ အောက်ပါ command ကို PyCharm project interpreter ဖြင့် run ပါ။

```bash
/home/htetmyatkyaw/PycharmProjects/Odoo_Training/.venv/bin/python /home/htetmyatkyaw/Documents/odoo/odoo-bin -c config/odoo.conf -d odoo_training -i training_task --stop-after-init
```

ပြီးလျှင် Odoo server ကို ဖွင့်ပါ။

```bash
/home/htetmyatkyaw/PycharmProjects/Odoo_Training/.venv/bin/python /home/htetmyatkyaw/Documents/odoo/odoo-bin -c config/odoo.conf -d odoo_training --http-interface=127.0.0.1
```

Browser မှာ `http://localhost:8069` ဖွင့်ပြီး **Training Tasks → Tasks → New** သို့သွားပါ။ Task အမည်တစ်ခုရေး၍ Save နှိပ်ပါ။ **Start Task** နှိပ်လျှင် In Progress၊ **Mark as Done** နှိပ်လျှင် Done အဆင့်သို့ ပြောင်းပါတယ်။

Wizard ကို စမ်းရန် **Training Tasks → Quick Task** ကိုနှိပ်ပါ။ Popup ထဲမှာ Task အမည်နဲ့ ရှင်းလင်းချက် ဖြည့်ပြီး **Create Task** နှိပ်လျှင် Task form အသစ်ကို ဖွင့်ပေးပါတယ်။ **Cancel** က Task မဖန်တီးဘဲ popup ပိတ်ပါတယ်။

Python model ကိုပြောင်းလျှင် server restart လုပ်ပါ။ CSV/XML/field ပြောင်းလျှင် `-i training_task` အစား `-u training_task` ဖြင့် module ကို upgrade လုပ်ပါ။
