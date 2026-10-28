# Screenshot build only: show 2 demo accounts and export the picker activity so adb can open it.
import pathlib

p = pathlib.Path('common/src/main/java/com/liskovsoft/smartyoutubetv2/common/app/presenters/dialogs/AccountSelectionPresenter.java')
s = p.read_text()
old = 'getView().update(mSignInService.getAccounts());'
assert old in s
demo = '''getView().update(java.util.Arrays.asList(
                    demoAccount(1, "Alex", "alex@example.com", "https://ui-avatars.com/api/?name=Alex&size=256&background=7b5ea7&color=fff", true),
                    demoAccount(2, "Sam", "sam@example.com", "https://ui-avatars.com/api/?name=Sam&size=256&background=e0803a&color=fff", false)));'''
s = s.replace(old, demo)
helper = '''
    private static Account demoAccount(int id, String name, String email, String avatar, boolean selected) {
        return new Account() {
            public int getId() { return id; }
            public String getName() { return name; }
            public String getEmail() { return email; }
            public String getAvatarImageUrl() { return avatar; }
            public boolean isSelected() { return selected; }
            public boolean isEmpty() { return false; }
        };
    }
'''
idx = s.rstrip().rfind('}')
s = s[:idx] + helper + '}\n'
p.write_text(s)

m = pathlib.Path('smarttubetv/src/main/AndroidManifest.xml')
t = m.read_text()
old = 'android:name="com.liskovsoft.smartyoutubetv2.tv.ui.accountselection.AccountSelectionActivity"'
assert old in t
m.write_text(t.replace(old, old + '\n                  android:exported="true"'))
print("demo patch applied")
