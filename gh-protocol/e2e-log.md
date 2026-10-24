## gh-protocol E2E log — 2026-10-24T18:20:47Z

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
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:packageDebugResources
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugResources
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugNativeLibs
> Task :app:processDebugResources
> Task :app:compressDebugAssets
> Task :app:mergeExtDexDebug

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:mergeLibDexDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:validateSigningDebug

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792863828109.json

BUILD SUCCESSFUL in 2m 31s
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
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 60s) ==
WARN: emulator CANNOT reach raw.githubusercontent.com (runner NAT) — pre-seeding app cache
cp: bad '/sdcard/ghsub.json': Permission denied
seeded cache:  bytes, meta=1792864601304
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2777)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
WARN: consent dialog never seen
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a141       2777   329   13785540 172172 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1      0 ::ffff:10.0.2.15:48394  ::ffff:172.217.116.:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{2942839 #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{108d800 u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(269, 661 - 812, 1741)
    isSleeping=false
    topResumedActivity=ActivityRecord{83edf39 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{83edf39 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{a805660 2777:com.ghprotocol.app/u0a141}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{2942839 #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~-YY_p0VOkBTnc9PhGhiJZA==/com.ghprotocol.app-xEeftIfljHgHIbnkhKJXbA==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.4 s.115 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.4 s.4 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.4 s.4 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} as.4 ?fontWeightAdjustment}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=false
      windows=[Window{fca637 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-20m59s382ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=false
    * Hist  #0: ActivityRecord{108d800 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{a805660 2777:com.ghprotocol.app/u0a141}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{2942839 #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~-YY_p0VOkBTnc9PhGhiJZA==/com.ghprotocol.app-xEeftIfljHgHIbnkhKJXbA==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.46 fontWeightAdjustment=0}
        mOverrideConfig={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.4 s.4 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=standard mAlwaysOnTop=undefined mRotation=undefined} as.4 ?fontWeightAdjustment}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=true
      windows=[Window{ce1319b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
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
    Resumed: ActivityRecord{83edf39 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{83edf39 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{2942839 #8 type=standard A=10141:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2146 rng=1080x1017-2146x2146
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@2560310
  deepestLastOrientationSource=ActivityRecord{83edf39 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h818dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 128 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.4 s.115 fontWeightAdjustment=0}
  mLayoutSeq=123
  mCurrentFocus=Window{453b4d8 u0 Application Not Responding: system}
  mFocusedApp=ActivityRecord{83edf39 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{fca637 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  Display areas in top down Z order:
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{2942839 #8 type=standard A=10141:com.ghprotocol.app}
      mLastFocusedRootTask=Task{2942839 #8 type=standard A=10141:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{2942839 #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{83edf39 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{108d800 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{468a1a4 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{8c6a845 #7 type=home I=com.android.launcher3/.uioverrides.QuickstepLauncher U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{5a264af u0 com.android.launcher3/.uioverrides.QuickstepLauncher t7}
      * Task{c88f6c #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{5e0df3b #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    mBottomGestureHost=Window{4d0d099 u0 NavigationBar0}
    mFocusedWindow=Window{453b4d8 u0 Application Not Responding: system}
    mTopFullscreenOpaqueWindowState=Window{fca637 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mNavBarColorWindowCandidate=Window{453b4d8 u0 Application Not Responding: system}
    mNavBarBackgroundWindow=Window{fca637 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{ bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{fca637 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,128][0,126], configInsets=[0,128][0,126], nonDecorFrame=[0,128][1080,2274], configFrame=[0,128][1080,2274]}
      ROTATION_90={nonDecorInsets=[128,0][126,0], configInsets=[128,63][126,0], nonDecorFrame=[128,0][2274,1080], configFrame=[128,63][2274,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,254], configInsets=[0,63][0,254], nonDecorFrame=[0,0][1080,2146], configFrame=[0,63][1080,2146]}
      ROTATION_270={nonDecorInsets=[126,0][128,0], configInsets=[126,63][128,0], nonDecorFrame=[126,0][2272,1080], configFrame=[126,63][2272,1080]}
--
        (multi-window) Task{6bde1ca #3 type=undefined}
        (multi-window) Task{5e0df3b #4 type=undefined}
        (fullscreen) Task{2942839 #8 type=standard A=10141:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{a805660 2777:com.ghprotocol.app/u0a141}]
  NumNonAppVisibleWindowUidMap:[ 10118:4 1000:2]
app filesDir/xray:
xray-err.log:
GhDiag (connect-flow trace):
--------- beginning of main
10-24 17:57:49.722  2777  2777 D GhDiag  : connect: tap -> CHECKING (have sub=false)
10-24 17:57:49.728  2777  2777 D GhDiag  : connect: fetching subscription (primary+mirror, timeouts 20s/30s)
10-24 17:58:28.783  2777  2777 D GhDiag  : connect: fetch result=false subscription update failed (primary + mirror)
10-24 17:58:28.797  2777  2777 D GhDiag  : connect: FAILED — no subscription available
=== E2E FAILED: tunnel not up (xray/:10808) ===


### e2e-logcat.log (crashes + app + vpn, tail)
pshots.MutableSnapshot, androidx.compose.runtime.snapshots.MutableSnapshot, androidx.compose.runtime.snapshots.SnapshotIdSet) took 143.557ms (2486.81 bytecodes/s) (8968B approximate peak alloc)
10-24 17:57:08.791   543   566 V WindowManager: Sent Transition #8 createdAt=10-24 17:57:05.195 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=625176 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{ab4fc1 Task{2942839 #8 type=standard A=10141:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=Rect(0, 128 - 0, 0) topActivityInfo=ActivityInfo{4727e66 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 17:57:08.887   543   566 V WindowManager:     info={id=8 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=STARTING_WINDOW_TRANSFER|FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{83edf39 u0 com.ghprotocol.app/.MainActivity)/@0xa85c7cb sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{108d800 u0 com.ghprotocol.app/.MainActivity)/@0xd59d29a sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 17:57:09.630   957   995 V WindowManagerShell: onTransitionReady android.os.BinderProxy@7af798e: {id=8 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=STARTING_WINDOW_TRANSFER|FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{83edf39 u0 com.ghprotocol.app/.MainActivity)/@0x4d0c08 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{108d800 u0 com.ghprotocol.app/.MainActivity)/@0xa8bfa1 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 17:57:10.577  2658  2658 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:57:16.383  2777  2777 W .ghprotocol.app: Verification of java.lang.Object kotlinx.coroutines.flow.FlowKt__ReduceKt.firstOrNull(kotlinx.coroutines.flow.Flow, kotlin.jvm.functions.Function2, kotlin.coroutines.Continuation) took 142.823ms (812.19 bytecodes/s) (4176B approximate peak alloc)
10-24 17:57:16.606  2777  2777 W .ghprotocol.app: Verification of void androidx.compose.ui.platform.AndroidComposeView.<init>(android.content.Context, kotlin.coroutines.CoroutineContext) took 102.735ms (8351.58 bytecodes/s) (30440B approximate peak alloc)
10-24 17:57:19.962   543  2832 E ActivityManager:   46% 2777/com.ghprotocol.app: 27% user + 18% kernel / faults: 237 minor
10-24 17:57:24.015  2777  2777 I .ghprotocol.app: Waiting for a blocking GC ClassLinker
10-24 17:57:24.085  2777  2791 I .ghprotocol.app: Background concurrent copying GC freed 8469(993KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 3171KB/6342KB, paused 97.190ms,185us total 2.650s
10-24 17:57:24.087  2777  2777 I .ghprotocol.app: WaitForGcToComplete blocked ClassLinker on Background for 72.247ms
10-24 17:57:27.942   543   570 W ActivityTaskManager: Activity stop timeout for ActivityRecord{108d800 u0 com.ghprotocol.app/.MainActivity t8}
10-24 17:57:28.302  2777  2777 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 17:57:28.302  2777  2777 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-24 17:57:28.302  2777  2777 W .ghprotocol.app: and incorrect proguard optimizations.
10-24 17:57:28.311  2777  2777 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 17:57:28.323  2777  2777 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 17:57:28.384  2777  2777 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 17:57:28.386  2777  2777 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 17:57:32.753  2777  2777 W .ghprotocol.app: Verification of void androidx.compose.material3.AppBarKt.SingleRowTopAppBar-cJHQLPU(androidx.compose.ui.Modifier, kotlin.jvm.functions.Function2, androidx.compose.ui.text.TextStyle, boolean, kotlin.jvm.functions.Function2, kotlin.jvm.functions.Function3, float, androidx.compose.foundation.layout.WindowInsets, androidx.compose.material3.TopAppBarColors, androidx.compose.material3.TopAppBarScrollBehavior, androidx.compose.runtime.Composer, int, int) took 113.573ms (8628.81 bytecodes/s) (28840B approximate peak alloc)
10-24 17:57:32.871   543  2269 D CoreBackPreview: Window{ce1319b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@4fe0689, mPriority=0, mIsAnimationCallback=false}
10-24 17:57:34.091  2777  2777 W .ghprotocol.app: Verification of void androidx.compose.foundation.text.BasicTextKt.BasicText-VhcvRP8(java.lang.String, androidx.compose.ui.Modifier, androidx.compose.ui.text.TextStyle, kotlin.jvm.functions.Function1, int, boolean, int, int, androidx.compose.ui.graphics.ColorProducer, androidx.compose.runtime.Composer, int, int) took 103.343ms (12066.53 bytecodes/s) (33864B approximate peak alloc)
10-24 17:57:36.453   543   570 I BLASTSyncEngine: Unfinished container: Task{2942839 #8 type=standard A=10141:com.ghprotocol.app}
10-24 17:57:37.412  2777  2777 W .ghprotocol.app: Verification of void androidx.compose.ui.text.android.TextLayout.<init>(java.lang.CharSequence, float, android.text.TextPaint, int, android.text.TextUtils$TruncateAt, int, float, float, boolean, boolean, int, int, int, int, int, int, int[], int[], androidx.compose.ui.text.android.LayoutIntrinsics) took 132.574ms (3477.28 bytecodes/s) (12048B approximate peak alloc)
10-24 17:57:39.136  2889  2889 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:57:39.498  2889  2889 I AndroidRuntime: Using default boot image
10-24 17:57:39.498  2889  2889 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:57:42.529  2777  2777 W .ghprotocol.app: Verification of androidx.compose.ui.draw.DrawResult androidx.compose.foundation.BorderKt.access$drawContentWithoutBorder(androidx.compose.ui.draw.CacheDrawScope) took 684.380ms (7.31 bytecodes/s) (1344B approximate peak alloc)
10-24 17:57:45.572  2777  2777 W .ghprotocol.app: Verification of java.lang.Object androidx.compose.foundation.layout.FlowLayoutKt$breakDownItems$nextSize$1$1.invoke(java.lang.Object) took 152.688ms (58.94 bytecodes/s) (1456B approximate peak alloc)
10-24 17:57:46.593  2889  2889 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:57:49.722  2777  2777 D GhDiag  : connect: tap -> CHECKING (have sub=false)
10-24 17:57:49.728  2777  2777 D GhDiag  : connect: fetching subscription (primary+mirror, timeouts 20s/30s)
10-24 17:57:50.842  2889  2889 D AndroidRuntime: Shutting down VM
10-24 17:57:52.257   543  2723 D CoreBackPreview: Window{845f3b3 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@500d4c1, mPriority=0, mIsAnimationCallback=false}
10-24 17:57:53.395   543  2946 E ActivityManager:   66% 2777/com.ghprotocol.app: 52% user + 14% kernel / faults: 363 minor
10-24 17:57:59.140  2777  2791 W .ghprotocol.app: Suspending all threads took: 5.340ms
10-24 17:58:00.198  2777  2791 I .ghprotocol.app: Background young concurrent copying GC freed 17057(1226KB) AllocSpace objects, 0(0B) LOS objects, 22% free, 4884KB/6342KB, paused 44.087ms,24.235ms total 3.877s
10-24 17:58:02.808  2777  2777 W .ghprotocol.app: Verification of androidx.compose.ui.graphics.colorspace.ColorSpace androidx.compose.ui.graphics.ColorSpaceVerificationHelper.composeColorSpace(android.graphics.ColorSpace) took 100.912ms (4776.42 bytecodes/s) (9840B approximate peak alloc)
10-24 17:58:03.437   543  1651 I WindowManager: finishDrawing of relaunch: Window{845f3b3 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity} 29330ms
10-24 17:58:03.726   543   566 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +59s724ms
10-24 17:58:04.136   543  2245 D CoreBackPreview: Window{aa278c7 u0 Splash Screen com.ghprotocol.app}: Setting back callback null
10-24 17:58:04.146   543  1651 W InputManager-JNI: Input channel object 'aa278c7 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-24 17:58:05.141  2777  3017 W .ghprotocol.app: Verification of boolean androidx.profileinstaller.ProfileInstaller.transcodeAndWrite(android.content.res.AssetManager, java.lang.String, android.content.pm.PackageInfo, java.io.File, java.lang.String, java.util.concurrent.Executor, androidx.profileinstaller.ProfileInstaller$DiagnosticsCallback) took 116.797ms (470.90 bytecodes/s) (2464B approximate peak alloc)
10-24 17:58:05.276  2777  3017 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-24 17:58:06.643   543  2245 D CoreBackPreview: Window{845f3b3 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback null
10-24 17:58:06.830   543  2269 W InputManager-JNI: Input channel object '845f3b3 com.ghprotocol.app/com.ghprotocol.app.MainActivity (client)' was disposed without first being removed with the input manager!
10-24 17:58:17.980   543  1651 D CoreBackPreview: Window{fca637 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@2689977, mPriority=0, mIsAnimationCallback=false}
10-24 17:58:20.951   543  3045 E ActivityManager:   35% 2777/com.ghprotocol.app: 20% user + 15% kernel / faults: 5967 minor
10-24 17:58:28.783  2777  2777 D GhDiag  : connect: fetch result=false subscription update failed (primary + mirror)
10-24 17:58:28.797  2777  2777 D GhDiag  : connect: FAILED — no subscription available
10-24 17:58:29.329   543  2178 I ActivityTaskManager: Activity reported stop, but no longer stopping: ActivityRecord{108d800 u0 com.ghprotocol.app/.MainActivity t8} STOPPED
10-24 17:58:30.091  3051  3051 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:58:30.388  3051  3051 I AndroidRuntime: Using default boot image
10-24 17:58:30.400  3051  3051 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:58:36.766  3051  3051 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:58:39.938  3051  3051 D AndroidRuntime: Shutting down VM
10-24 17:59:15.647  3220  3220 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:59:16.157  3220  3220 I AndroidRuntime: Using default boot image
10-24 17:59:16.158  3220  3220 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:59:23.047  3220  3220 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:59:25.998  3220  3220 D AndroidRuntime: Shutting down VM
10-24 17:59:40.840   543   570 I BLASTSyncEngine: Unfinished container: Task{2942839 #8 type=standard A=10141:com.ghprotocol.app}
10-24 17:59:55.986   543   603 I AppsFilter: interaction: PackageSetting{1400cb5 com.ghprotocol.app/10141} -> PackageSetting{522bf4a com.android.cellbroadcastreceiver.module/10131} BLOCKED
10-24 18:00:02.587  3254  3254 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:00:02.987  3354  3354 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:00:03.418  3354  3354 I AndroidRuntime: Using default boot image
10-24 18:00:03.419  3354  3354 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:00:11.487  3354  3354 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:00:14.789  3354  3354 D AndroidRuntime: Shutting down VM
10-24 18:00:53.500  3474  3474 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:00:53.733  3474  3474 I AndroidRuntime: Using default boot image
10-24 18:00:53.734  3474  3474 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:00:58.795  3474  3474 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:01:01.246  3474  3474 D AndroidRuntime: Shutting down VM
10-24 18:01:32.241  3631  3631 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:01:32.440  3631  3631 I AndroidRuntime: Using default boot image
10-24 18:01:32.442  3631  3631 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:01:38.763  3631  3631 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:01:42.814  3631  3631 D AndroidRuntime: Shutting down VM
10-24 18:01:46.600  3492  3492 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:02:21.671  3726  3726 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:02:21.859  3726  3726 I AndroidRuntime: Using default boot image
10-24 18:02:21.864  3726  3726 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:02:23.714  3653  3653 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:02:28.867  3726  3726 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:02:31.256  3726  3726 D AndroidRuntime: Shutting down VM
10-24 18:02:51.090  3730  3730 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:03:03.985  3833  3833 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:03:04.419  3833  3833 I AndroidRuntime: Using default boot image
10-24 18:03:04.433  3833  3833 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:03:12.151  3833  3833 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:03:14.915  3833  3833 D AndroidRuntime: Shutting down VM
10-24 18:03:21.438  3812  3812 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:03:48.455  3972  3972 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:03:48.677  3972  3972 I AndroidRuntime: Using default boot image
10-24 18:03:48.678  3972  3972 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:03:54.974  3972  3972 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:03:58.427  3972  3972 D AndroidRuntime: Shutting down VM
10-24 18:04:02.925  3900  3900 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:04:32.001  4073  4073 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:04:32.238  4073  4073 I AndroidRuntime: Using default boot image
10-24 18:04:32.238  4073  4073 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:04:38.054  4073  4073 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:04:39.355  3999  3999 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:04:40.615  4073  4073 D AndroidRuntime: Shutting down VM
10-24 18:05:08.595  4093  4093 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:05:10.335  4163  4163 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:05:10.555  4163  4163 I AndroidRuntime: Using default boot image
10-24 18:05:10.555  4163  4163 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:05:14.791  4163  4163 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:05:17.246  4163  4163 D AndroidRuntime: Shutting down VM
10-24 18:05:40.449  4168  4168 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:05:50.437  4263  4263 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:05:50.641  4263  4263 I AndroidRuntime: Using default boot image
10-24 18:05:50.642  4263  4263 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:05:57.016  4263  4263 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:05:59.643  4263  4263 D AndroidRuntime: Shutting down VM
10-24 18:06:16.232  4247  4247 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:06:34.730  4383  4383 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:06:35.016  4383  4383 I AndroidRuntime: Using default boot image
10-24 18:06:35.018  4383  4383 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:06:41.381  4383  4383 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:06:45.031  4383  4383 D AndroidRuntime: Shutting down VM
10-24 18:06:46.999  4337  4337 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:07:14.519  4417  4417 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:07:18.834  4488  4488 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:07:19.015  4488  4488 I AndroidRuntime: Using default boot image
10-24 18:07:19.021  4488  4488 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:07:24.273  4488  4488 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:07:27.391  4488  4488 D AndroidRuntime: Shutting down VM
10-24 18:07:48.249  4491  4491 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:08:03.901  4611  4611 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:08:04.126  4611  4611 I AndroidRuntime: Using default boot image
10-24 18:08:04.127  4611  4611 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:08:10.562  4611  4611 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:08:13.274  4611  4611 D AndroidRuntime: Shutting down VM
10-24 18:08:17.963  4571  4571 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:08:46.833  4733  4733 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:08:47.118  4733  4733 I AndroidRuntime: Using default boot image
10-24 18:08:47.123  4733  4733 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:08:50.878  4658  4658 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:08:54.045  4733  4733 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:08:56.185  4733  4733 D AndroidRuntime: Shutting down VM
10-24 18:09:16.302  4741  4741 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:09:32.016  4845  4845 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:09:32.233  4845  4845 I AndroidRuntime: Using default boot image
10-24 18:09:32.234  4845  4845 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:09:37.266  4845  4845 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:09:41.244  4845  4845 D AndroidRuntime: Shutting down VM
10-24 18:09:47.139  4824  4824 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:10:15.999  4970  4970 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:10:16.360  4970  4970 I AndroidRuntime: Using default boot image
10-24 18:10:16.361  4970  4970 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:10:23.314  4904  4904 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:10:23.669  4970  4970 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:10:26.517  4970  4970 D AndroidRuntime: Shutting down VM
10-24 18:11:02.654  5071  5071 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:11:03.028  5071  5071 I AndroidRuntime: Using default boot image
10-24 18:11:03.029  5071  5071 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:11:03.135  4995  4995 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:11:08.619  5071  5071 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:11:10.815  5071  5071 D AndroidRuntime: Shutting down VM
10-24 18:11:34.429  5078  5078 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:11:43.873  5179  5179 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:11:44.092  5179  5179 I AndroidRuntime: Using default boot image
10-24 18:11:44.094  5179  5179 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:11:50.655  5179  5179 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:11:53.181  5179  5179 D AndroidRuntime: Shutting down VM
10-24 18:12:16.592  5165  5165 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:12:27.475  5280  5280 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:12:27.883  5280  5280 I AndroidRuntime: Using default boot image
10-24 18:12:27.883  5280  5280 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:12:35.739  5280  5280 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:12:38.023  5280  5280 D AndroidRuntime: Shutting down VM
10-24 18:12:49.126  5264  5264 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:13:15.506  5426  5426 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:13:15.782  5426  5426 I AndroidRuntime: Using default boot image
10-24 18:13:15.788  5426  5426 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:13:19.727  5350  5350 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:13:21.799  5426  5426 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:13:24.162  5426  5426 D AndroidRuntime: Shutting down VM
10-24 18:13:36.998  2777  2791 W .ghprotocol.app: Suspending all threads took: 9.978ms
10-24 18:13:37.247  2777  2791 W .ghprotocol.app: Cleared Reference was only reachable from finalizer (only reported once)
10-24 18:13:37.679  2777  2791 I .ghprotocol.app: Background concurrent copying GC freed 23254(1049KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 5689KB/11MB, paused 13.266ms,11.547ms total 3.359s
10-24 18:13:47.340  2777  5498 W .ghprotocol.app: Long monitor contention with owner DefaultDispatcher-worker-1 (2875) at void sun.security.provider.X509Factory.addToCache(sun.security.util.Cache, byte[], java.lang.Object)(X509Factory.java:232) waiters=0 in sun.security.x509.X509CertImpl sun.security.provider.X509Factory.intern(java.security.cert.X509Certificate) for 157ms
10-24 18:13:52.477  2777  2875 W .ghprotocol.app: Long monitor contention with owner DefaultDispatcher-worker-2 (2873) at java.lang.Object sun.security.provider.X509Factory.getFromCache(sun.security.util.Cache, byte[])(X509Factory.java:219) waiters=0 in sun.security.x509.X509CertImpl sun.security.provider.X509Factory.intern(java.security.cert.X509Certificate) for 142ms
10-24 18:13:54.133  5441  5441 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:14:03.771  5536  5536 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:14:03.965  5536  5536 I AndroidRuntime: Using default boot image
10-24 18:14:03.966  5536  5536 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:14:13.615  5536  5536 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:14:16.308  5536  5536 D AndroidRuntime: Shutting down VM
10-24 18:14:17.417  2777  2791 W .ghprotocol.app: Suspending all threads took: 8.159ms
10-24 18:14:17.705  2777  2791 I .ghprotocol.app: Background young concurrent copying GC freed 102614(3919KB) AllocSpace objects, 4(80KB) LOS objects, 38% free, 6997KB/11MB, paused 20.838ms,8.669ms total 1.649s
10-24 18:14:27.682  5529  5529 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:14:52.284  5624  5624 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:14:53.109  5687  5687 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:14:53.499  5687  5687 I AndroidRuntime: Using default boot image
10-24 18:14:53.505  5687  5687 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:14:58.909  5687  5687 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:15:01.067  5687  5687 D AndroidRuntime: Shutting down VM
10-24 18:15:21.542  5693  5693 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:15:33.373  5807  5807 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:15:33.652  5807  5807 I AndroidRuntime: Using default boot image
10-24 18:15:33.652  5807  5807 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:15:39.515  5807  5807 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:15:41.666  5807  5807 D AndroidRuntime: Shutting down VM
10-24 18:15:51.826  5785  5785 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:16:14.561  5941  5941 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:16:14.805  5941  5941 I AndroidRuntime: Using default boot image
10-24 18:16:14.806  5941  5941 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:16:20.583  5878  5878 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:16:21.501  5941  5941 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:16:23.679  5941  5941 D AndroidRuntime: Shutting down VM
10-24 18:16:42.242  5964  5964 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:17:00.817  6086  6086 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:17:01.151  6086  6086 I AndroidRuntime: Using default boot image
10-24 18:17:01.157  6086  6086 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:17:08.763  6086  6086 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:17:12.446  6086  6086 D AndroidRuntime: Shutting down VM
10-24 18:17:12.794  6030  6030 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:17:45.381  6162  6162 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:17:45.555  6162  6162 I AndroidRuntime: Using default boot image
10-24 18:17:45.555  6162  6162 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:17:50.582  6162  6162 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:17:52.689  6162  6162 D AndroidRuntime: Shutting down VM
10-24 18:18:11.109  6166  6166 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:18:23.477  6305  6305 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:18:23.869  6305  6305 I AndroidRuntime: Using default boot image
10-24 18:18:23.869  6305  6305 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:18:29.819  6305  6305 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:18:32.478  6305  6305 D AndroidRuntime: Shutting down VM
10-24 18:18:41.870  6283  6283 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:19:06.198  6439  6439 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 18:19:06.506  6439  6439 I AndroidRuntime: Using default boot image
10-24 18:19:06.507  6439  6439 I AndroidRuntime: Leaving lock profiling enabled
10-24 18:19:11.686  6376  6376 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:19:12.222  6439  6439 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 18:19:14.400  6439  6439 D AndroidRuntime: Shutting down VM
10-24 18:19:36.425  6459  6459 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 18:20:07.278  6538  6538 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.


