## gh-protocol E2E log — 2026-10-24T17:40:29Z

### gradle-build.log (tail)
Downloading https://services.gradle.org/distributions/gradle-8.10.2-bin.zip
.............10%.............20%.............30%.............40%.............50%.............60%.............70%.............80%.............90%.............100%

Welcome to Gradle 8.10.2!

Here are the highlights of this release:
 - Support for Java 23
 - Faster configuration cache
 - Better configuration cache reports

For more details see https://docs.gradle.org/8.10.2/release-notes.html

To honour the JVM settings for this build a single-use Daemon process will be forked. For more on this, please refer to https://docs.gradle.org/8.10.2/userguide/gradle_daemon.html#sec:disabling_the_daemon in the Gradle documentation.
Daemon will be stopped at the end of the build 
Calculating task graph as no cached configuration is available for tasks: assembleDebug
> Task :app:preBuild UP-TO-DATE
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:parseDebugLocalResources
> Task :app:mapDebugSourceSetPaths
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:checkDebugAarMetadata
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugJniLibFolders
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugResources
> Task :app:mergeDebugNativeLibs
> Task :app:mergeDebugAssets
> Task :app:mergeLibDexDebug

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:processDebugResources
> Task :app:compressDebugAssets
> Task :app:mergeExtDexDebug
> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_2-1792861847505.json

BUILD SUCCESSFUL in 2m 14s
37 actionable tasks: 37 executed
Configuration cache entry stored.

### e2e.log
== adb devices ==
== wait for emulator to reach device state ==
emulator ready after ~4s
List of devices attached
emulator-5554	device

== install APK ==
Performing Streamed Install
Success
== wait for emulator external network (needed for subscription fetch) ==
emulator has network after ~4s (icmp=no validated=8)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2356)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
WARN: consent dialog never seen
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a141       2356   326   13801068 169452 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6      25      0 ::ffff:10.0.2.15:50128  ::ffff:140.82.114.3:443 CLOSE_WAIT 
tcp6       0      0 ::ffff:10.0.2.15:38106  ::ffff:142.251.154.:443 ESTABLISHED
tcp6       0      0 ::ffff:10.0.2.15:38102  ::ffff:142.251.154.:443 ESTABLISHED
tcp6      32      0 ::ffff:10.0.2.15:49004  ::ffff:5.106.4.1:443    CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.15:57840  ::ffff:172.217.118.:443 CLOSE_WAIT 
tcp6      25      0 ::ffff:10.0.2.15:36512  ::ffff:140.82.114.3:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{d4269be u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(297, 660 - 783, 1740)
    isSleeping=false
    topResumedActivity=ActivityRecord{c60ef60 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{c60ef60 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{4ed36eb 2356:com.ghprotocol.app/u0a141}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~IHgX50Xa7dJ4kTlsXALuCA==/com.ghprotocol.app-7mQO6OwX5ygJeWUGiAfUxw==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.5 s.117 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.5 s.4 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.5 s.4 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} as.5 ?fontWeightAdjustment}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=false
      windows=[Window{583c2bd u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-17m28s577ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=false
    * Hist  #0: ActivityRecord{d4269be u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{4ed36eb 2356:com.ghprotocol.app/u0a141}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~IHgX50Xa7dJ4kTlsXALuCA==/com.ghprotocol.app-7mQO6OwX5ygJeWUGiAfUxw==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.3 s.51 fontWeightAdjustment=0}
        mOverrideConfig={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.3 s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.5 s.5 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=standard mAlwaysOnTop=undefined mRotation=undefined} as.5 ?fontWeightAdjustment}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=true
      windows=[Window{ea3aa95 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      startingWindow=null startingSurface=null startingDisplayed=false startingMoved=true mVisibleSetFromTransferredStartingWindow=false
      resizeMode=RESIZE_MODE_RESIZEABLE_VIA_SDK_VERSION
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{c60ef60 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{c60ef60 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2146 rng=1080x1017-2146x2146
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@23894351
  deepestLastOrientationSource=ActivityRecord{c60ef60 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.5 s.117 fontWeightAdjustment=0}
  mLayoutSeq=118
  mCurrentFocus=Window{ce933a3 u0 Application Not Responding: system}
  mFocusedApp=ActivityRecord{c60ef60 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{583c2bd u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  Display areas in top down Z order:
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app}
      mLastFocusedRootTask=Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{c60ef60 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{d4269be u0 com.ghprotocol.app/.MainActivity t8}
      * Task{f9e7de5 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{e1539c0 #7 type=home I=com.android.launcher3/.uioverrides.QuickstepLauncher U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{29aaf43 u0 com.android.launcher3/.uioverrides.QuickstepLauncher t7}
      * Task{8dd7961 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{82622e3 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    mBottomGestureHost=Window{6d80540 u0 NavigationBar0}
    mFocusedWindow=Window{ce933a3 u0 Application Not Responding: system}
    mTopFullscreenOpaqueWindowState=Window{583c2bd u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mNavBarColorWindowCandidate=Window{ce933a3 u0 Application Not Responding: system}
    mNavBarBackgroundWindow=Window{583c2bd u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{ bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{583c2bd u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,128][0,126], configInsets=[0,128][0,126], nonDecorFrame=[0,128][1080,2274], configFrame=[0,128][1080,2274]}
      ROTATION_90={nonDecorInsets=[128,0][126,0], configInsets=[128,63][126,0], nonDecorFrame=[128,0][2274,1080], configFrame=[128,63][2274,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,254], configInsets=[0,63][0,254], nonDecorFrame=[0,0][1080,2146], configFrame=[0,63][1080,2146]}
      ROTATION_270={nonDecorInsets=[126,0][128,0], configInsets=[126,63][128,0], nonDecorFrame=[126,0][2272,1080], configFrame=[126,63][2272,1080]}
--
        (multi-window) Task{3193947 #3 type=undefined}
        (multi-window) Task{82622e3 #4 type=undefined}
        (fullscreen) Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{4ed36eb 2356:com.ghprotocol.app/u0a141}]
  NumNonAppVisibleWindowUidMap:[ 10117:4 1000:2]
app filesDir/xray:
xray-err.log:
GhDiag (connect-flow trace):
--------- beginning of main
10-24 17:21:40.534  2356  2356 D GhDiag  : connect: tap -> CHECKING (have sub=false)
10-24 17:21:40.535  2356  2356 D GhDiag  : connect: fetching subscription (primary+mirror, timeouts 20s/30s)
10-24 17:22:06.962  2356  2356 D GhDiag  : connect: fetch result=false subscription update failed (primary + mirror)
10-24 17:22:06.973  2356  2356 D GhDiag  : connect: FAILED — no subscription available
=== E2E FAILED: tunnel not up (xray/:10808) ===


### e2e-logcat.log (crashes + app + vpn, tail)
.369   534  1096 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-24 17:21:03.596   534   561 W ActivityTaskManager: Activity top resumed state loss timeout for ActivityRecord{d4269be u0 com.ghprotocol.app/.MainActivity t8}
10-24 17:21:03.646   534   561 W ActivityTaskManager: Activity pause timeout for ActivityRecord{d4269be u0 com.ghprotocol.app/.MainActivity t8}
10-24 17:21:04.405   917   950 V WindowManagerShell: onTransitionReady android.os.BinderProxy@b9c11a5: {id=8 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=STARTING_WINDOW_TRANSFER|FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{c60ef60 u0 com.ghprotocol.app/.MainActivity)/@0xee67ea3 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{d4269be u0 com.ghprotocol.app/.MainActivity)/@0x7cbc5a0 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 17:21:05.102   534   558 V WindowManager: Sent Transition #8 createdAt=10-24 17:21:02.943 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=437183 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{ef05482 Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=Rect(0, 128 - 0, 0) topActivityInfo=ActivityInfo{9abf031 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 17:21:05.147   534   558 V WindowManager:     info={id=8 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=STARTING_WINDOW_TRANSFER|FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{c60ef60 u0 com.ghprotocol.app/.MainActivity)/@0xfe710f2 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{d4269be u0 com.ghprotocol.app/.MainActivity)/@0xa117bfd sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 17:21:06.417  2356  2356 W .ghprotocol.app: Verification of java.lang.Object kotlin.text.StringsKt__StringNumberConversionsJVMKt.screenFloatValue$StringsKt__StringNumberConversionsJVMKt(java.lang.String, kotlin.jvm.functions.Function1) took 119.445ms (200.93 bytecodes/s) (2168B approximate peak alloc)
10-24 17:21:10.485   534   593 I AppsFilter: interaction: PackageSetting{98cafe9 com.ghprotocol.app/10141} -> PackageSetting{5b6146e com.android.inputmethod.latin/10108} BLOCKED
10-24 17:21:15.704   534   593 I AppsFilter: interaction: PackageSetting{98cafe9 com.ghprotocol.app/10141} -> PackageSetting{e34abea com.android.calendar/10101} BLOCKED
10-24 17:21:16.325   534   561 W ActivityTaskManager: Activity stop timeout for ActivityRecord{d4269be u0 com.ghprotocol.app/.MainActivity t8}
10-24 17:21:17.130  2356  2490 W .ghprotocol.app: Long monitor contention with owner DefaultDispatcher-worker-1 (2488) at javax.net.SocketFactory javax.net.ssl.SSLSocketFactory.getDefault()(SSLSocketFactory.java:156) waiters=0 in javax.net.SocketFactory javax.net.ssl.SSLSocketFactory.getDefault() for 452ms
10-24 17:21:18.474   534   593 I AppsFilter: interaction: PackageSetting{98cafe9 com.ghprotocol.app/10141} -> PackageSetting{1814238 com.android.camera2/10105} BLOCKED
10-24 17:21:18.731  2356  2356 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 17:21:18.731  2356  2356 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-24 17:21:18.731  2356  2356 W .ghprotocol.app: and incorrect proguard optimizations.
10-24 17:21:18.741  2356  2356 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 17:21:18.742  2356  2356 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 17:21:18.743  2356  2356 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 17:21:18.755  2356  2356 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 17:21:22.564  2356  2356 W .ghprotocol.app: Verification of void androidx.compose.runtime.snapshots.SnapshotStateObserver$ObservedScopeMap.notifyInvalidatedScopes() took 100.819ms (1170.41 bytecodes/s) (4256B approximate peak alloc)
10-24 17:21:22.750  2356  2356 W .ghprotocol.app: Verification of boolean androidx.compose.runtime.snapshots.SnapshotStateObserver$ObservedScopeMap.recordInvalidation(java.util.Set) took 184.057ms (13615.31 bytecodes/s) (69232B approximate peak alloc)
10-24 17:21:23.649   534   980 D CoreBackPreview: Window{ea3aa95 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@c3dc72d, mPriority=0, mIsAnimationCallback=false}
10-24 17:21:24.572  2356  2356 W .ghprotocol.app: Verification of void androidx.compose.material3.ComposableSingletons$AppBarKt.<clinit>() took 184.962ms (1313.78 bytecodes/s) (4280B approximate peak alloc)
10-24 17:21:26.275  2356  2356 W .ghprotocol.app: Verification of void androidx.compose.material3.IconButtonKt.FilledTonalIconToggleButton(boolean, kotlin.jvm.functions.Function1, androidx.compose.ui.Modifier, boolean, androidx.compose.ui.graphics.Shape, androidx.compose.material3.IconToggleButtonColors, androidx.compose.foundation.interaction.MutableInteractionSource, kotlin.jvm.functions.Function2, androidx.compose.runtime.Composer, int, int) took 194.527ms (3104.96 bytecodes/s) (17000B approximate peak alloc)
10-24 17:21:27.644  2356  2356 W .ghprotocol.app: Verification of long androidx.compose.ui.draw.PainterNode.modifyConstraints-ZezNO4M(long) took 132.796ms (1460.89 bytecodes/s) (4912B approximate peak alloc)
10-24 17:21:28.501  2356  2356 W .ghprotocol.app: Verification of void androidx.compose.foundation.layout.RowMeasurePolicy$placeHelper$1$1.invoke(androidx.compose.ui.layout.Placeable$PlacementScope) took 264.846ms (252.98 bytecodes/s) (2824B approximate peak alloc)
10-24 17:21:29.598  2356  2365 I .ghprotocol.app: Background concurrent copying GC freed 14930(1518KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 3975KB/7950KB, paused 97.460ms,76us total 5.715s
10-24 17:21:29.731  2535  2535 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:21:29.969  2535  2535 I AndroidRuntime: Using default boot image
10-24 17:21:29.973  2535  2535 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:21:30.967  2356  2356 W .ghprotocol.app: Verification of void com.ghprotocol.app.ui.HomeScreenKt$StatusCard$1.invoke(androidx.compose.foundation.layout.ColumnScope, androidx.compose.runtime.Composer, int) took 112.539ms (7846.17 bytecodes/s) (19656B approximate peak alloc)
10-24 17:21:35.828   534   561 I BLASTSyncEngine: Unfinished container: Task{8731a1f #8 type=standard A=10141:com.ghprotocol.app}
10-24 17:21:35.904  2535  2535 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:21:40.046  2535  2535 D AndroidRuntime: Shutting down VM
10-24 17:21:40.534  2356  2356 D GhDiag  : connect: tap -> CHECKING (have sub=false)
10-24 17:21:40.535  2356  2356 D GhDiag  : connect: fetching subscription (primary+mirror, timeouts 20s/30s)
10-24 17:21:42.881   534  2226 D CoreBackPreview: Window{c043513 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@e32ad7d, mPriority=0, mIsAnimationCallback=false}
10-24 17:21:43.621   534  2559 E ActivityManager:   51% 2356/com.ghprotocol.app: 35% user + 15% kernel / faults: 405 minor
10-24 17:21:50.459   534  1557 I WindowManager: finishDrawing of relaunch: Window{c043513 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity} 19398ms
10-24 17:21:50.767   534   558 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +48s231ms
10-24 17:21:51.539   534  1559 W InputManager-JNI: Input channel object 'd5612b8 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-24 17:21:51.618   534   593 I AppsFilter: interaction: PackageSetting{d36fb1c com.ghprotocol.app/10141} -> PackageSetting{493a325 com.android.rkpdapp/10139} BLOCKED
10-24 17:21:52.587  2356  2693 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-24 17:21:52.973   534  1559 D CoreBackPreview: Window{c043513 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback null
10-24 17:21:52.988  2356  2693 W .ghprotocol.app: Verification of androidx.profileinstaller.ProfileVerifier$CompilationStatus androidx.profileinstaller.ProfileVerifier.writeProfileVerification(android.content.Context, boolean) took 165.869ms (1694.11 bytecodes/s) (10000B approximate peak alloc)
10-24 17:21:52.998   534  1559 W InputManager-JNI: Input channel object 'c043513 com.ghprotocol.app/com.ghprotocol.app.MainActivity (client)' was disposed without first being removed with the input manager!
10-24 17:21:53.155  2356  2693 W .ghprotocol.app: Verification of java.lang.Object androidx.concurrent.futures.AbstractResolvableFuture.get() took 147.348ms (699.02 bytecodes/s) (3912B approximate peak alloc)
10-24 17:21:53.829   534   593 I AppsFilter: interaction: PackageSetting{d36fb1c com.ghprotocol.app/10141} -> PackageSetting{df65e6f com.android.rkpdapp/10139} BLOCKED
10-24 17:21:54.535   534  1508 I ActivityTaskManager: Activity reported stop, but no longer stopping: ActivityRecord{d4269be u0 com.ghprotocol.app/.MainActivity t8} STOPPED
10-24 17:21:58.124   534  1508 D CoreBackPreview: Window{583c2bd u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@3d66955, mPriority=0, mIsAnimationCallback=false}
10-24 17:22:06.962  2356  2356 D GhDiag  : connect: fetch result=false subscription update failed (primary + mirror)
10-24 17:22:06.973  2356  2356 D GhDiag  : connect: FAILED — no subscription available
10-24 17:22:13.776  2762  2762 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:22:14.018  2762  2762 I AndroidRuntime: Using default boot image
10-24 17:22:14.019  2762  2762 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:22:18.946   534  2783 E ActivityManager:   37% 2356/com.ghprotocol.app: 21% user + 15% kernel / faults: 7264 minor 1 major
10-24 17:22:19.394  2762  2762 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:22:23.171  2762  2762 D AndroidRuntime: Shutting down VM
10-24 17:22:51.604  2934  2934 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:22:51.804  2934  2934 I AndroidRuntime: Using default boot image
10-24 17:22:51.805  2934  2934 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:22:56.782  2934  2934 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:22:59.233  2934  2934 D AndroidRuntime: Shutting down VM
10-24 17:23:08.727  2824  2824 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:23:29.729  3098  3098 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:23:29.978  3098  3098 I AndroidRuntime: Using default boot image
10-24 17:23:29.985  3098  3098 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:23:35.184  3098  3098 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:23:37.184  3098  3098 D AndroidRuntime: Shutting down VM
10-24 17:23:49.776  3007  3007 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:24:08.118  3190  3190 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:24:08.265  3190  3190 I AndroidRuntime: Using default boot image
10-24 17:24:08.265  3190  3190 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:24:13.367  3190  3190 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:24:16.511  3190  3190 D AndroidRuntime: Shutting down VM
10-24 17:24:17.212   534   593 I AppsFilter: interaction: PackageSetting{d36fb1c com.ghprotocol.app/10141} -> PackageSetting{bb1d428 com.android.cellbroadcastreceiver.module/10137} BLOCKED
10-24 17:24:44.810  3279  3279 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:24:45.027  3279  3279 I AndroidRuntime: Using default boot image
10-24 17:24:45.032  3279  3279 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:24:50.608  3279  3279 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:24:53.073  3279  3279 D AndroidRuntime: Shutting down VM
10-24 17:25:24.192  3387  3387 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:25:24.565  3387  3387 I AndroidRuntime: Using default boot image
10-24 17:25:24.566  3387  3387 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:25:28.774  3387  3387 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:25:31.038  3387  3387 D AndroidRuntime: Shutting down VM
10-24 17:26:00.509  3513  3513 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:26:00.646  3513  3513 I AndroidRuntime: Using default boot image
10-24 17:26:00.650  3513  3513 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:26:04.433  3513  3513 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:26:07.480  3513  3513 D AndroidRuntime: Shutting down VM
10-24 17:26:11.026  3455  3455 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:26:36.308  3618  3618 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:26:36.883  3618  3618 I AndroidRuntime: Using default boot image
10-24 17:26:36.897  3618  3618 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:26:38.304  3540  3540 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:26:42.291  3618  3618 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:26:44.721  3618  3618 D AndroidRuntime: Shutting down VM
10-24 17:27:07.028  3624  3624 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:27:13.119  3723  3723 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:27:13.311  3723  3723 I AndroidRuntime: Using default boot image
10-24 17:27:13.318  3723  3723 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:27:17.114  3723  3723 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:27:19.062  3723  3723 D AndroidRuntime: Shutting down VM
10-24 17:27:34.154  3725  3725 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:27:49.423  3868  3868 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:27:49.610  3868  3868 I AndroidRuntime: Using default boot image
10-24 17:27:49.611  3868  3868 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:27:54.322  3868  3868 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:27:56.576  3868  3868 D AndroidRuntime: Shutting down VM
10-24 17:28:00.617  3816  3816 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:28:25.820  3901  3901 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:28:26.615  3969  3969 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:28:26.903  3969  3969 I AndroidRuntime: Using default boot image
10-24 17:28:26.909  3969  3969 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:28:31.561  3969  3969 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:28:33.966  3969  3969 D AndroidRuntime: Shutting down VM
10-24 17:28:57.848  3974  3974 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:29:01.569  4067  4067 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:29:01.742  4067  4067 I AndroidRuntime: Using default boot image
10-24 17:29:01.742  4067  4067 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:29:07.245  4067  4067 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:29:09.819  4067  4067 D AndroidRuntime: Shutting down VM
10-24 17:29:29.424  4070  4070 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:29:41.172  4191  4191 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:29:41.542  4191  4191 I AndroidRuntime: Using default boot image
10-24 17:29:41.542  4191  4191 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:29:45.540  4191  4191 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:29:48.457  4191  4191 D AndroidRuntime: Shutting down VM
10-24 17:29:54.418  4155  4155 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:30:18.582  4308  4308 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:30:18.771  4308  4308 I AndroidRuntime: Using default boot image
10-24 17:30:18.771  4308  4308 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:30:23.409  4240  4240 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:30:23.579  4308  4308 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:30:26.388  4308  4308 D AndroidRuntime: Shutting down VM
10-24 17:30:45.893  4328  4328 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:30:55.477  4413  4413 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:30:55.661  4413  4413 I AndroidRuntime: Using default boot image
10-24 17:30:55.661  4413  4413 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:30:59.521  4413  4413 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:31:02.555  4413  4413 D AndroidRuntime: Shutting down VM
10-24 17:31:12.143  4396  4396 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:31:34.110  4542  4542 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:31:34.289  4542  4542 I AndroidRuntime: Using default boot image
10-24 17:31:34.289  4542  4542 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:31:37.879  4542  4542 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:31:40.706  4542  4542 D AndroidRuntime: Shutting down VM
10-24 17:31:42.627  4476  4476 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:32:07.161  4637  4637 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:32:07.282  4637  4637 I AndroidRuntime: Using default boot image
10-24 17:32:07.282  4637  4637 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:32:08.977  4571  4571 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:32:13.047  4637  4637 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:32:15.341  4637  4637 D AndroidRuntime: Shutting down VM
10-24 17:32:35.636  4642  4642 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:32:45.514  4752  4752 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:32:45.762  4752  4752 I AndroidRuntime: Using default boot image
10-24 17:32:45.765  4752  4752 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:32:51.394  4752  4752 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:32:53.965  4752  4752 D AndroidRuntime: Shutting down VM
10-24 17:33:01.263  4734  4734 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:33:23.655  4880  4880 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:33:23.967  4880  4880 I AndroidRuntime: Using default boot image
10-24 17:33:23.979  4880  4880 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:33:26.747  4816  4816 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:33:28.302  4880  4880 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:33:30.817  4880  4880 D AndroidRuntime: Shutting down VM
10-24 17:33:47.663  4896  4896 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:33:58.356  5012  5012 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:33:58.530  5012  5012 I AndroidRuntime: Using default boot image
10-24 17:33:58.531  5012  5012 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:34:03.368  5012  5012 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:34:05.523  5012  5012 D AndroidRuntime: Shutting down VM
10-24 17:34:10.818  4967  4967 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:34:32.772  5124  5124 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:34:33.018  5124  5124 I AndroidRuntime: Using default boot image
10-24 17:34:33.018  5124  5124 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:34:37.664  5049  5049 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:34:38.315  5124  5124 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:34:41.029  5124  5124 D AndroidRuntime: Shutting down VM
10-24 17:35:02.407  5144  5144 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:35:08.583  5223  5223 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:35:08.750  5223  5223 I AndroidRuntime: Using default boot image
10-24 17:35:08.756  5223  5223 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:35:13.695  5223  5223 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:35:15.664  5223  5223 D AndroidRuntime: Shutting down VM
10-24 17:35:33.771  5212  5212 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:35:44.158  5324  5324 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:35:44.295  5324  5324 I AndroidRuntime: Using default boot image
10-24 17:35:44.295  5324  5324 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:35:47.830  5324  5324 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:35:50.069  5324  5324 D AndroidRuntime: Shutting down VM
10-24 17:35:58.523  5308  5308 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:36:17.818  5462  5462 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:36:18.008  5462  5462 I AndroidRuntime: Using default boot image
10-24 17:36:18.013  5462  5462 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:36:20.870  5395  5395 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:36:22.474  5462  5462 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:36:24.427  5462  5462 D AndroidRuntime: Shutting down VM
10-24 17:36:43.245  5483  5483 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:36:52.785  5573  5573 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:36:53.186  5573  5573 I AndroidRuntime: Using default boot image
10-24 17:36:53.186  5573  5573 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:36:56.558  5573  5573 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:36:59.791  5573  5573 D AndroidRuntime: Shutting down VM
10-24 17:37:05.548  5556  5556 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:37:14.876  2356  2365 W .ghprotocol.app: Suspending all threads took: 19.502ms
10-24 17:37:15.065  2356  2365 W .ghprotocol.app: Cleared Reference was only reachable from finalizer (only reported once)
10-24 17:37:15.265  2356  2365 I .ghprotocol.app: Background young concurrent copying GC freed 42859(1989KB) AllocSpace objects, 0(0B) LOS objects, 25% free, 5907KB/7950KB, paused 875us,20.064ms total 1.911s
10-24 17:37:24.619  2356  2365 I .ghprotocol.app: Background young concurrent copying GC freed 36639(1440KB) AllocSpace objects, 0(0B) LOS objects, 21% free, 6261KB/7950KB, paused 213us,436us total 1.037s
10-24 17:37:29.223  5726  5726 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:37:29.450  5726  5726 I AndroidRuntime: Using default boot image
10-24 17:37:29.456  5726  5726 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:37:33.595  5726  5726 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:37:36.956  5726  5726 D AndroidRuntime: Shutting down VM
10-24 17:37:37.272  5642  5642 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:37:40.121  2356  2365 W .ghprotocol.app: Suspending all threads took: 17.048ms
10-24 17:37:40.141  2356  2365 I .ghprotocol.app: Background young concurrent copying GC freed 30497(1264KB) AllocSpace objects, 0(0B) LOS objects, 15% free, 6680KB/7950KB, paused 10.709ms,17.636ms total 673.801ms
10-24 17:37:46.988  2356  2365 W .ghprotocol.app: Suspending all threads took: 7.637ms
10-24 17:37:47.025  2356  2365 I .ghprotocol.app: Background young concurrent copying GC freed 22151(867KB) AllocSpace objects, 2(40KB) LOS objects, 11% free, 7070KB/7950KB, paused 17.281ms,8.064ms total 757.045ms
10-24 17:37:49.761  2356  2365 I .ghprotocol.app: Background young concurrent copying GC freed 15513(627KB) AllocSpace objects, 2(40KB) LOS objects, 8% free, 7308KB/7950KB, paused 8.578ms,4.106ms total 440.941ms
10-24 17:38:05.595  5846  5846 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:38:05.743  5846  5846 I AndroidRuntime: Using default boot image
10-24 17:38:05.744  5846  5846 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:38:10.319  5846  5846 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:38:10.995  5758  5758 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:38:11.982  5846  5846 D AndroidRuntime: Shutting down VM
10-24 17:38:31.046  5864  5864 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:38:39.467  5965  5965 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:38:39.643  5965  5965 I AndroidRuntime: Using default boot image
10-24 17:38:39.643  5965  5965 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:38:44.185  5965  5965 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:38:46.782  5965  5965 D AndroidRuntime: Shutting down VM
10-24 17:38:53.261  5946  5946 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:39:14.139  6040  6040 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:39:15.573  6115  6115 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:39:15.786  6115  6115 I AndroidRuntime: Using default boot image
10-24 17:39:15.794  6115  6115 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:39:20.603  6115  6115 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:39:23.025  6115  6115 D AndroidRuntime: Shutting down VM
10-24 17:39:44.120  6119  6119 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:40:14.957  6222  6222 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.


